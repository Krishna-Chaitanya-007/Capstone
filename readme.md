# 👁️ FaceGuard: Real-Time Liveness, Auth & Emotion AI

FaceGuard is a sophisticated, real-time security application built with Python and modern AI libraries. It verifies a user's identity by combining:
1.  **Active Liveness Detection:** Prevents spoofing from photos or videos using a random challenge-response system.
2.  **Facial Recognition:** Registers and authenticates users against a secure face database.
3.  **Emotion Analysis:** Provides a continuous, live feed of the user's detected emotion after successful login.

---

## 🚀 Core Features

* **✅ Active Liveness Detection:** Employs a secure challenge-response mechanism (e.g., "Blink," "Smile") to ensure the user is a live person.
* **🔐 Facial Recognition & Auth:** Securely register new users and log in existing ones using facial biometrics.
* **😊 Real-time Emotion Analysis:** After successful login, the system provides a continuous, live feed of the user's detected emotion (e.g., Happy, Sad, Neutral).
* **📂 File-Based Database:** Uses a simple folder-based system for storing user faces, managed by DeepFace.

---

## 🛠️ Technology Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Flask, OpenCV, Dlib, DeepFace |
| **Frontend** | HTML, Tailwind CSS, JavaScript |
| **AI Models** | Dlib 68-point Landmark Predictor, VGG-Face |

---

## 🏁 Getting Started

This guide will walk you through setting up and running the entire project from scratch using the **Anaconda Prompt**.

### Prerequisites

Before you begin, ensure you have the following software installed on your machine:

1.  [**Anaconda**](https://www.anaconda.com/download)
2.  [**Git**](https://git-scm.com/downloads)

### Installation & Setup Guide

Follow these steps exactly in your Anaconda Prompt.

**1. Clone the Repository**

First, clone this repository to your local machine. This will be **slow** because it includes the large `.dat` model file, but it's the simplest way.

```bash
# Clone the repository
git clone [https://github.com/Krishna-Chaitanya-007/Capstone.git](https://github.com/Krishna-Chaitanya-007/Capstone.git)

# Navigate into the project folder
cd Capstone
```

**2. Create the Conda Environment**

We will create a dedicated environment named faceguard to keep all the complex libraries separate.


```bash
# Create a new environment with Python 3.10
conda create -n faceguard python=3.10 -y

# Activate the new environment
conda activate faceguard
```
Your prompt should now look like (faceguard) D:\...


**3. Install Dependencies**

These AI libraries can be tricky to install. This method is the most reliable.


```bash
# 1. Install dlib, opencv, and flask from the conda-forge channel
conda install -c conda-forge dlib opencv flask -y

# 2. Install deepface using pip (which is inside your conda env)
pip install deepface
```
**4. Run the Application**
You're all set! Now, just run the Flask server.


```bash
# (Make sure you are still in the (faceguard) environment)
python app.py
```
You will see output in your terminal indicating the server is running, probably on http://127.0.0.1:5000.

📖 How to Use the Application
Once the server is running, open your web browser (like Chrome or Firefox) and go to:
```
http://127.0.0.1:5000
```
You must grant camera permission when the browser asks.

<br/>

**1. How to Register a New User** 
``` markdown
Click the Register button.

The text input field will appear. Type your name (e.g., "Krishna").

Click the "Click to Start Registration" button.

The liveness check will begin. Follow the on-screen command (e.g., "Blink").

If you pass, you will see "✅ Liveness Confirmed!" followed by "Authenticating..."

The system will save your face under your name. You will see "Registration Complete!"
```

**2. How to Log In**
``` markdown
From the main screen (or after clicking Reset), click the Login button.

The liveness check will begin. Follow the on-screen command.

If you pass, you will see "✅ Liveness Confirmed!" followed by "Authenticating..."

The system will compare your face to all registered users.

If you are recognized, you will see "Welcome, [YourName]!"

The application will immediately switch to the Live Emotion Analysis feed, drawing a box over your face and showing your current emotion.
```

3. Resetting
```
If a liveness check fails, or after you are done, click the Reset button to return to the main registration/login screen.
```
<hr/>
<br/>

**⚠️ Common Troubleshooting:**
``` 
Error installing dlib:

  -> If the conda install command fails, you are likely missing C++ build tools.

  -> Install Visual Studio Build Tools.

  -> When installing, check the "Desktop development with C++" workload.

  -> Restart your computer.

  -> Try the conda install command again.
```

```
Camera Not Working:

  -> Make sure you clicked "Allow" when your browser asked for camera permission.

  -> Make sure no other application (like Zoom or Teams) is using your camera.

  -> Try refreshing the page (F5)
```
