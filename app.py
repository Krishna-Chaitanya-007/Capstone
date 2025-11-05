# File: app.py
import os
import cv2
import dlib
import numpy as np
from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import base64
import random
import logging

# Setup
logging.basicConfig(level=logging.INFO)
app = Flask(__name__, template_folder='.')

# Model path
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
if not os.path.exists(PREDICTOR_PATH):
    logging.error(f"FATAL ERROR: Dlib landmark model not found at '{PREDICTOR_PATH}'")
    logging.error("Please download it from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
    raise SystemExit(1)

# Load models
try:
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    logging.info("Dlib models loaded successfully.")
except Exception as e:
    logging.error(f"Error loading dlib models: {e}")
    raise

# --- New: Face Database Path ---
DB_PATH = "face_database"
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH, exist_ok=True)
    logging.info(f"Created face database at: {DB_PATH}")
# --- End New ---

# Liveness challenges
CHALLENGES = ['Blink', 'Smile', 'Look Left', 'Look Right']

# Eye aspect ratio
def get_eye_aspect_ratio(eye_landmarks):
    A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
    B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
    C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
    if C == 0:
        return 0.0
    return (A + B) / (2.0 * C)

# choose largest face rect
def largest_rect(rects):
    if not rects:
        return None
    areas = [(r.right() - r.left()) * (r.bottom() - r.top()) for r in rects]
    idx = int(np.argmax(areas))
    return rects[idx]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_challenge')
def get_challenge():
    challenge = random.choice(CHALLENGES)
    logging.info(f"Issuing new challenge: {challenge}")
    return jsonify({'challenge': challenge})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json or {}
    image_data_url = data.get('image')
    challenge = data.get('challenge')

    if not image_data_url or not challenge:
        return jsonify({'success': False, 'reason': 'Missing data'}), 400

    # decode image
    try:
        img_data = base64.b64decode(image_data_url.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("imdecode returned None")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logging.warning(f"Invalid image format: {e}")
        return jsonify({'success': False, 'reason': 'Invalid image format'}), 400

    rects = detector(gray, 0)
    rect = largest_rect(rects)
    if rect is None:
        return jsonify({'success': False, 'reason': 'No face detected'})

    landmarks = predictor(gray, rect)
    success = False

    try:
        if challenge == 'Blink':
            left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
            right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
            ear = (get_eye_aspect_ratio(left_eye) + get_eye_aspect_ratio(right_eye)) / 2.0
            logging.debug(f"EAR: {ear:.3f}")
            if ear < 0.20:
                success = True

        elif challenge == 'Smile':
            # use smaller frame for speed
            small = cv2.resize(frame, (0, 0), fx=0.6, fy=0.6)
            try:
                dfres = DeepFace.analyze(small, actions=['emotion'], enforce_detection=False, detector_backend='dlib')
                # DeepFace may return dict or list; normalize
                if isinstance(dfres, dict):
                    dominant = dfres.get('dominant_emotion', '')
                elif isinstance(dfres, list) and len(dfres) > 0:
                    dominant = dfres[0].get('dominant_emotion', '')
                else:
                    dominant = ''
                logging.debug(f"Smile dominant emotion: {dominant}")
                if dominant and dominant.lower() == 'happy':
                    success = True
            except Exception as e:
                logging.warning(f"DeepFace analyze error (smile challenge): {e}")
                success = False

        elif challenge in ('Look Left', 'Look Right'):

            # --- NEW LOGIC ---
            # We measure the internal geometry of the face to detect rotation,
            # not just the nose's position in the frame.

            # Get relevant landmarks
            nose = landmarks.part(33)
            left_jaw = landmarks.part(2)  # User's right, viewer's left
            right_jaw = landmarks.part(14) # User's left, viewer's right

            # Calculate horizontal distances from nose to jaw edges
            # We use abs() just in case, but .x should be fine
            dist_nose_to_left_jaw = abs(nose.x - left_jaw.x)
            dist_nose_to_right_jaw = abs(nose.x - right_jaw.x)

            # Avoid a divide-by-zero error
            # ...
            if dist_nose_to_right_jaw == 0 or dist_nose_to_left_jaw == 0:
                success = False
            else:
                # Calculate the turn ratio
                turn_ratio = dist_nose_to_left_jaw / dist_nose_to_right_jaw
                logging.debug(f"Turn Ratio (Left/Right): {turn_ratio:.3f}")

                # --- CORRECTED LOGIC ---
                if challenge == 'Look Left':
                    # User turns to screen's left -> ratio gets SMALL
                    if turn_ratio < 0.55: 
                        success = True

                else:  # Look Right
                    # User turns to screen's right -> ratio gets LARGE
                    if turn_ratio > 1.8: 
                        success = True
            # --- END CORRECTED LOGIC ---

    except Exception as e:
        logging.warning(f"Error during verification logic: {e}")
        success = False

    if success:
        logging.info(f"Challenge '{challenge}' PASSED.")
    else:
        logging.info(f"Challenge '{challenge}' FAILED.")

    return jsonify({'success': bool(success)})

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    image_data_url = (request.json or {}).get('image')
    if not image_data_url:
        return jsonify({'error': 'No image data'}), 400

    try:
        img_data = base64.b64decode(image_data_url.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("imdecode returned None")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logging.warning(f"Invalid image format in analyze_emotion: {e}")
        return jsonify({'error': 'Invalid image format'}), 400

    rects = detector(gray, 0)
    rect = largest_rect(rects)
    if rect is None:
        return jsonify({'emotion': 'N/A', 'box': []})

    box = [rect.left(), rect.top(), rect.right(), rect.bottom()]

    emotion = "N/A"
    try:
        # resize for speed
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        result = DeepFace.analyze(small, actions=['emotion'], enforce_detection=False, detector_backend='dlib')
        if isinstance(result, dict):
            dominant = result.get('dominant_emotion', '')
        elif isinstance(result, list) and len(result) > 0:
            dominant = result[0].get('dominant_emotion', '')
        else:
            dominant = ''
        if dominant:
            emotion = dominant.capitalize()
    except Exception as e:
        logging.warning(f"DeepFace failed during continuous analysis: {e}")

    return jsonify({'emotion': emotion, 'box': box})


# --- New Authentication Endpoints ---

@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    image_data_url = data.get('image')
    username = data.get('username')

    if not image_data_url or not username:
        return jsonify({'success': False, 'reason': 'Missing image or username'}), 400

    # Sanitize username to create a safe filename
    safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
    if not safe_username:
        return jsonify({'success': False, 'reason': 'Invalid username'}), 400
    
    filename = f"{safe_username}.jpg"
    filepath = os.path.join(DB_PATH, filename)

    # Decode image
    try:
        img_data = base64.b64decode(image_data_url.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("imdecode returned None")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logging.warning(f"Invalid image format in register: {e}")
        return jsonify({'success': False, 'reason': 'Invalid image format'}), 400

    # Check for a face
    rects = detector(gray, 0)
    if not rects:
        return jsonify({'success': False, 'reason': 'No face detected for registration'})

    # Save the image
    try:
        cv2.imwrite(filepath, frame)
        
        # Important: Delete old pickle files so DeepFace re-indexes on next login
        pkl_files = [f for f in os.listdir(DB_PATH) if f.endswith(".pkl")]
        for f in pkl_files:
            os.remove(os.path.join(DB_PATH, f))
        
        logging.info(f"Registered new user: {safe_username}")
        return jsonify({'success': True, 'message': f'User {safe_username} registered.'})
    except Exception as e:
        logging.error(f"Failed to save image or clear index: {e}")
        return jsonify({'success': False, 'reason': 'Failed to save user data.'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    image_data_url = data.get('image')

    if not image_data_url:
        return jsonify({'success': False, 'reason': 'Missing image'}), 400

    # Decode image
    try:
        img_data = base64.b64decode(image_data_url.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("imdecode returned None")
    except Exception as e:
        logging.warning(f"Invalid image format in login: {e}")
        return jsonify({'success': False, 'reason': 'Invalid image format'}), 400

    # Find face
    try:
        # DeepFace.find will search the DB_PATH for the face in 'frame'
        # It handles indexing (creating .pkl files) automatically
        # We use 'VGG-Face' as it's a good balance of speed and accuracy
        dfs = DeepFace.find(img_path=frame, 
                            db_path=DB_PATH, 
                            model_name='VGG-Face',
                            enforce_detection=False,
                            detector_backend='dlib')
        
        if not dfs or dfs[0].empty:
            logging.info("Login attempt: User not recognized.")
            return jsonify({'success': False, 'reason': 'User not recognized'})

        # Get the path of the best match
        identity_path = dfs[0]['identity'].iloc[0]
        
        # Extract username from the filename (e.g., "face_database/Krishna.jpg" -> "Krishna")
        username = os.path.basename(identity_path).split('.')[0]
        
        logging.info(f"Login successful: User {username} recognized.")
        return jsonify({'success': True, 'username': username})

    except Exception as e:
        logging.error(f"DeepFace.find error during login: {e}")
        return jsonify({'success': False, 'reason': 'An error occurred during face matching.'})

# --- End New Endpoints ---


if __name__ == '__main__':
    # Enable threaded to allow concurrent requests during dev; in production use WSGI server
    app.run(debug=True, threaded=True)