from flask import Flask, request, render_template, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

IMG_SIZE = 128
CLASS_NAMES = ["rock", "paper", "scissors"]

model = load_model("rps_model.h5")

app = Flask(__name__)

UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            return render_template("index.html", error="Будь ласка, виберіть файл!")

        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        result = CLASS_NAMES[np.argmax(prediction)]

        return render_template("result.html", filename=file.filename, result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
