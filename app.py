import os
from datetime import datetime
from flask import Flask, render_template, request

from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


@app.route("/", methods=["GET", "POST"])
def home():

    image_name = None
    result = None
    confidence = None

    print("Request received:", request.method)

    if request.method == "POST":

        print("POST detected")

        if "image" in request.files:

            image = request.files["image"]

            if image.filename == "":

                print("No file selected")

            else:

                print("Filename:", image.filename)
                safe_name = secure_filename(image.filename)

                extension = image.filename.rsplit(".", 1)[1].lower()

                if extension in ALLOWED_EXTENSIONS:

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    new_filename = (
                        timestamp + "_" + safe_name
                    )

                    file_path = os.path.join(
                        UPLOAD_FOLDER,
                        new_filename
                    )

                    image.save(file_path)
                    image_name = new_filename
                    result = "Deepfake Detected"
                    confidence = 95 
                    

                    print("Image saved successfully")
                    print("Saved as:", new_filename)

                else:

                    print("Only JPG, JPEG and PNG files are allowed")

        else:

            print("No image uploaded")

    return render_template(
        "index.html",
        project="DeepFakeChain",
        image_name=image_name,
        result=result,
        confidence=confidence
    )


if __name__ == "__main__":
    app.run(debug=True)