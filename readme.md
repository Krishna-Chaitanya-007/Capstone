👁️ FaceGuard: Real-Time Liveness & Emotion AI
A sophisticated, real-time security application built with Python and modern AI libraries. FaceGuard verifies user liveness through an interactive challenge-response system and performs continuous emotion analysis.

It's highly recommended to record a short GIF of the app working and place it here. This makes your project look incredibly professional.

🚀 Core Features
✅ Active Liveness Detection: Employs a secure challenge-response mechanism (e.g., "Smile," "Blink") to prevent spoofing from photos and videos.

✅ Real-time Emotion Analysis: After successful liveness verification, the system provides a continuous, live feed of the user's detected emotion.

✅ Responsive UI: A clean, modern web interface built with Tailwind CSS that provides clear instructions and feedback to the user.

✅ Robust Backend: Powered by a Flask server, capable of handling real-time video stream processing.


🛠️ Technology Stack
Category

Technology

Backend



AI / ML



Frontend



🏁 Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
This project has a complex setup process due to C++ library compilation. Following these steps in order is crucial for a successful installation.

You will need the following tools installed on your Windows machine:

Python (3.8 - 3.11 recommended)

Git for version control

CMake for building C++ libraries

Visual Studio Build Tools (with the C++ workload)

Note: For a detailed, step-by-step guide on setting up these prerequisites on a completely fresh machine, please see the Detailed Setup Guide below.

🚀 Quick Installation & Launch
If your prerequisites are already installed, you can launch the application with these commands.

Clone the repository:

```
git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd YourRepoName
````

Install Python packages:
```
pip install -r requirements.txt
```
Stuck on dlib? If the pip install fails, use Conda: conda install -c conda-forge dlib

Download the Dlib Model:

Download the facial landmark model from this link.

Unzip it and place the shape_predictor_68_face_landmarks.dat file in the root of the project folder.

Run the application:

python app.py

Open in your browser:

Navigate to http://127.0.0.1:5000

🛠️ Detailed Setup Guide (For a Fresh Windows Install)
If you are starting from scratch, follow these steps carefully.

<details>
<summary><strong>Click to expand the full setup guide</strong></summary>

Install Python:

Download Python (e.g., 3.10.x) from python.org.

CRUCIAL: During installation, you must check the box that says "Add Python to PATH".

Install Git:

Download and install Git from git-scm.com.

Install CMake:

Download the "Windows x64 Installer" from cmake.org.

CRUCIAL: During installation, select the option "Add CMake to the system PATH for all users".

Install Visual Studio Build Tools:

Go to the Visual Studio downloads page and find "Tools for Visual Studio".

Download the "Build Tools for Visual Studio".

Run the installer. In the "Workloads" tab, you must select "Desktop development with C++". This provides the necessary C++ compiler.

After the installation is complete, RESTART YOUR COMPUTER. This step is not optional.

Follow the Quick Installation & Launch steps above. After completing these prerequisites, the "Quick Installation" commands will now work successfully.

</details>

🗺️ Project Roadmap
This project is under active development. Future enhancements include:

[ ] Face Recognition & Database Integration:

[ ] Add a user registration flow.

[ ] Store face embeddings in a database.

[ ] Implement a verification step to grant access only to registered users.

[ ] Add More Liveness Challenges: Implement additional challenges like "Turn Head Left/Right" or "Raise Eyebrows" to increase security.

[ ] UI/UX Enhancements: Refine the user interface for a smoother, more intuitive experience.

Feel free to contribute to this project by submitting a pull request.
