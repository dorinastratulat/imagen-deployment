import os

from flask import Flask, make_response, render_template, redirect, request

import uuid

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel


PROJECT_ID = "duet-roadshow-test-6"
LOCATION = "us-central1"  

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    conv_id = str(uuid.uuid4())
    return render_template("home.html", conv_id=conv_id)


@app.route("/<conv_id>", methods=["GET"])
def show_image(conv_id):
    return render_template("index.html", conv_id=conv_id, pict_url="/img/image.png")


@app.route("/<conv_id>", methods=["POST"])
def create_image(conv_id):
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    generation_model = ImageGenerationModel.from_pretrained("imagegeneration@006")

    prompt = request.form["desc"]
    #prompt = "aerial shot of a river flowing up a valley full of flowers"

    response = generation_model.generate_images(prompt=prompt,)
    image = response.images[0]

    image.save(f"./{conv_id}.png", include_generation_parameters=False)  #  This must be wrong.
    return render_template("index.html", conv_id=conv_id)


@app.route("/img/<img_id>", methods=["GET"]) 
def fetch_img(img_id):
    with open(img_id, "rb") as f:
        img = f.read()

    resp = make_response(img, "200")
    resp.headers['Content-type'] = "image/png"
    return resp

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))