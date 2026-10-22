import os
from datetime import datetime
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
from math import gcd
import cv2

app = Flask(__name__)
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if(face_cascade.empty()):
    print("Error loading cascade classifier")
else:
    print("Cascade classifier loaded successfully")

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


@app.route("/", methods=["GET", "POST"])
def home():
    
    print("HOME FUNCTION CALLED")

    image_name = None
    result = None
    confidence = None
    width = None
    height = None
    image_format = None
    file_size = None
    aspect_ratio = None
    analysis_summary = None
    average_brightness = None
    facecount=None
    annotated_name=None

    print("Request received:", request.method)

    if request.method == "POST":

        print("POST detected")

        if "image" in request.files:

            image = request.files["image"]

            if image.filename == "":

                print("No file selected")

            else:

                print("Filename:", image.filename)

                safe_name = secure_filename(
                    image.filename
                )

                extension = image.filename.rsplit(
                    ".", 1
                )[1].lower()

                if extension in ALLOWED_EXTENSIONS:

                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )

                    new_filename = (
                        timestamp + "_" + safe_name
                    )

                    file_path = os.path.join(
                        UPLOAD_FOLDER,
                        new_filename
                    )

                    image.save(file_path)
                    opencv_image = cv2.imread(file_path)
                    original_image=opencv_image.copy()
                    if opencv_image is not None:
                        height_cv, width_cv, channels = opencv_image.shape 
                        gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray_image,
                                scaleFactor=1.1,
                                minNeighbors=6,
                                minSize=(50, 50)
                            )
                        facecount=len(faces)
                        print("Detected faces:", len(faces))
                        print("Face count variable:", facecount)
                        for (x,y,width,height) in faces: 
                            face_crop = original_image[y:y+height, x:x+width]
                            face_filename = f"face_{x}_{y}_{width}_{height}.jpg"
                            face_path = os.path.join(UPLOAD_FOLDER, face_filename)
                            saved_face = cv2.imwrite(face_path, face_crop)
                            cv2.rectangle(opencv_image,(x,y),(x+width,y+height),(255,0,0),2)

                        annotated_filename= "annotated_" + new_filename
                        annotated_path=os.path.join(UPLOAD_FOLDER, annotated_filename)
                        saved=cv2.imwrite(annotated_path, opencv_image)
                        annotated_name=annotated_filename
                        print("Annotated image path:", annotated_path)
                        print("Annotated image saved:", saved)
                                                      

                                   
                        rgb_image=cv2.cvtColor(opencv_image,cv2.COLOR_BGR2RGB)
                        average_brightness = gray_image.mean()
                    else:
                        analysis_summary = "Error: Unable to read the image using OpenCV."

                    image_name = new_filename

                    result = "Deepfake Detected"

                    confidence = 95

                    uploaded_image = Image.open(
                        file_path
                    )

                    width, height = (
                        uploaded_image.size
                    )

                    common_divisor = gcd(
                       width,
                       height
                    )
                    aspect_ratio = (
                        f"{width // common_divisor}"
                        f":"
                        f"{height // common_divisor}"
                    )
                    #f is formatted string



                    image_format = (
                        uploaded_image.format
                    )

                    file_size = os.path.getsize(
                        file_path
                    )

                    file_size = round(
                        file_size / (1024 * 1024),
                        2
                    )
                    analysis_summary = (
                        f"This is a {image_format} image "
                        f"with dimensions {width}x{height} "
                        f"and a file size of {file_size} MB. "
                        f"The aspect ratio is {aspect_ratio}."
                    )



                    print("Width:", width)
                    print("Height:", height)
                    print("Format:", image_format)
                    print("File Size:", file_size, "MB")

                    print(
                        "Image saved successfully"
                    )

                    print(
                        "Saved as:",
                        new_filename
                    )

                else:

                    print(
                        "Only JPG, JPEG and PNG files are allowed"
                    )

        else:

            print("No image uploaded")

    return render_template(
        "index.html",
        project="DeepFakeChain",
        image_name=image_name,
        result=result,
        confidence=confidence,
        width=width,
        height=height,
        image_format=image_format,
        file_size=file_size,
        analysis_summary=analysis_summary,
        average_brightness=average_brightness,
        facecount=facecount,
        
        aspect_ratio=aspect_ratio,
        annotated_name=annotated_name

        
    )


if __name__ == "__main__":
    app.run(debug=True)
