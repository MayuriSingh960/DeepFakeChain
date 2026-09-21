
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    project_name = "DeepFakeChain"

    return render_template(
        "index.html",
        project=project_name
    )

if __name__ == "__main__":
    app.run(debug=True)