from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    print("Request received:", request.method)

    if request.method == "POST":
        print("POST detected")

        image = request.files["image"]

        print("Filename:", image.filename)

    return render_template(
        "index.html",
        project="DeepFakeChain"
    )

if __name__ == "__main__":
    app.run(debug=True)