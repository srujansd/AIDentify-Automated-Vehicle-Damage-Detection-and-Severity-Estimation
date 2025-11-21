AIDentify – Automated Vehicle Damage Detection & Severity Estimation

AIDentify is an AI-powered system that automates vehicle damage detection using the YOLOv8 deep learning model. It identifies damages such as dents, scratches, cracks, and broken parts from images, video files, or real-time webcam input. The goal is to reduce manual inspection time and improve accuracy in insurance claim assessments.

This project integrates a Flask web application that enables users to upload media and receive instant detection results with bounding boxes and confidence scores.

🚀 Features

YOLOv8-based damage detection

Detects dents, scratches, cracks, and other external damages

Real-time inference for images, videos, and webcam streams

High accuracy with a trained model achieving 91.3% mAP

Flask-based interactive web interface

Supports custom datasets and easy retraining

🧠 Model Performance

Dataset Size: 778 annotated vehicle images

mAP: 91.3%

Precision: 89.5%

Recall: 92.1%

Average inference time: ~1.2 seconds/frame

🛠 Tech Stack

Python 3

YOLOv8 (Ultralytics)

PyTorch

Flask

OpenCV

HTML, CSS, JavaScript

📁 Project Structure
AIDentify/
│── dataset/               # Training images & annotations
│── models/                # YOLOv8 model files
│── static/                # Frontend static assets
│── templates/             # HTML templates
│── app.py                 # Flask backend
│── detect.py              # Inference script
│── train.py               # Model training script
│── requirements.txt       # Dependencies
│── README.md              # Documentation

🔧 Installation & Setup
1. Clone the Repository
git clone https://github.com/yourusername/AIDentify.git
cd AIDentify

2. Install Dependencies
pip install -r requirements.txt

3. Download Model Weights

Place your trained YOLOv8 weights (e.g., best.pt) inside the models directory.

4. Run the Flask Application
python app.py

5. Access the Web Interface

Open your browser and visit:

http://127.0.0.1:5000

🎥 How It Works

User uploads an image/video or uses webcam.

Backend loads the YOLOv8 model.

Model performs real-time damage detection.

Damage regions are highlighted with bounding boxes.

Output is displayed instantly on the web interface.

📈 Results

Detects common vehicle damages: dents, scratches, cracks, broken parts etc,..

Works effectively under various lighting conditions

Performs better than older models like YOLOv5 and SSD

🔮 Future Enhancements

Automatic damage severity rating

Repair cost estimation

Cloud deployment (AWS/GCP/Azure)

Android/iOS mobile app

Larger dataset for additional damage categories
