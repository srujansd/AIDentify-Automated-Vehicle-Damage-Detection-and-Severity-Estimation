
# Render-ready replacement based on your uploaded app.py

import argparse
import io
import os
import base64
import traceback
import cv2
from flask import Flask, flash, render_template, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)
app.secret_key = "damage-detection-secret-key"

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
model = YOLO("best.pt")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        results = model(frame)
        annotated = results[0].plot()
        _, jpeg = cv2.imencode(".jpg", annotated)
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
               jpeg.tobytes() + b"\r\n")
    cap.release()


@app.route("/")
@app.route("/first")
def first():
    return render_template("first.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/chart")
def chart():
    return render_template("chart.html")


@app.route("/performance")
def performance():
    return render_template("performance.html")


@app.route("/image")
def image():
    return render_template("image.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            flash("No file selected")
            return redirect(url_for("image"))

        file = request.files["file"]

        if file.filename == "":
            flash("Please choose an image")
            return redirect(url_for("image"))

        if not allowed_file(file.filename):
            flash("Only JPG/JPEG/PNG files are allowed")
            return redirect(url_for("image"))

        img = Image.open(file).convert("RGB")
        results = model.predict(source=img, verbose=False)

        plotted = results[0].plot()
        out = Image.fromarray(plotted)

        buf = io.BytesIO()
        out.save(buf, format="PNG")
        buf.seek(0)

        return render_template(
            "image.html",
            detection_results=base64.b64encode(buf.read()).decode("utf-8")
        )
    except Exception:
        print(traceback.format_exc())
        return "<pre>" + traceback.format_exc() + "</pre>", 500


@app.route("/video")
def video():
    return render_template("video.html")


@app.route("/predict_img", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST" and "file" in request.files:
        f = request.files["file"]
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        path = os.path.join(upload_dir, secure_filename(f.filename))
        f.save(path)

        if path.lower().endswith(".mp4"):
            cap = cv2.VideoCapture(path)
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(
                "output.mp4",
                cv2.VideoWriter_fourcc(*"mp4v"),
                30,
                (w, h),
            )

            while cap.isOpened():
                ok, frame = cap.read()
                if not ok:
                    break
                res = model(frame)
                out.write(res[0].plot())

            cap.release()
            out.release()

        return redirect(url_for("video"))

    return render_template("video.html")


@app.route("/webcam")
def webcam():
    return render_template("webcam.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/stop", methods=["POST"])
def stop():
    return render_template("first.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=5000, type=int)
    args = parser.parse_args()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", args.port))
    )
