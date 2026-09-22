import os
from flask import Flask, render_template, request

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"


@app.route("/", methods=["GET", "POST"])
def home():

    print("Request received:", request.method)

    if request.method == "POST":

        print("POST detected")

        if "image" in request.files:

            image = request.files["image"]

            if image.filename == "":

                print("No file selected")

            else:

                print("Filename:", image.filename)

                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    image.filename
                )

                image.save(file_path)

                print("Image saved successfully")

        else:

            print("No image uploaded")

    return render_template(
        "index.html",
        project="DeepFakeChain"
    )


if __name__ == "__main__":
    app.run(debug=True)