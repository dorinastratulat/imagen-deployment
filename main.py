import flask
import tempfile
import base64
from vertexai.vision_models import ImageGenerationModel

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    return flask.render_template("home.html")

@app.route("/", methods=["POST"])
def display_image():
    # Code to get the prompt (called prompt) from the submitted form
    prompt = flask.request.form["prompt"]

    # Code to generate the image
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    response = model.generate_images(prompt=prompt)[0]

    # Code to create a URL for the image (called image_url)
    with tempfile.NamedTemporaryFile("wb") as f:
        filename = f.name
        response.save(filename, include_generation_parameters=False)
        # process the saved file here, before it goes away
        with open(filename, "rb") as image_file:
            binary_image = image_file.read()
            base64_image = base64.b64encode(binary_image).decode("utf-8")
            image_uri = f"data:image/png;base64,{base64_image}"

    # image_uri = "https://preview.redd.it/camouflage-v0-hy4y2pigsrde1.jpeg?auto=webp&s=cb21b48eb3c0ed5aa714b6523b23e4271d44e6e6"

    return flask.render_template("display.html", prompt=prompt, image_uri=image_uri)

# Initialize the web server app when the code locally (Cloud Run handles it in that environment)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)