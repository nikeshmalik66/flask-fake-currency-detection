from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image
import io

app = Flask(__name__)

generation_config = {
  "temperature": 0.1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]


API_KEY = 'AIzaSyAnBGGRvbIWM6DYkEIvXGxqWMlIRCZLB6A'
genai.configure(api_key=API_KEY)

def compress_image(image_bytes, quality=20):
    # Open image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    # Compress and convert the image to bytes
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=quality)
    return output.getvalue()
  
# app routes and api endpoints

# for index
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fake-currency")
def ocrHandwriting():
    return render_template("ocr-recognition.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    bytes_data = file.read()

    # Compress the image
    compressed_bytes = compress_image(bytes_data, quality=40)
    
    
    # Create and configure the model
    model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
    # Generate content
    response = model.generate_content(
        glm.Content(
            parts=[
                glm.Part(text="When you receive an image of a currency note, your role is to meticulously examine the note to verify its legitimacy. Pay close attention to the serial number and the note's security features for this analysis. For serial numbers OVR 798647 or 5GF 766797, the note should immediately be classified as 'Fake Currency' due to a previous determination of these being counterfeit identifiers. If a note with a different serial number is uploaded, deploy your analytical capabilities to scrutinize the currency. Should your assessment conclude that the note is counterfeit, declare it 'Fake Currency.' Conversely, if the note is deemed authentic, confirm it as 'Real Currency' and provide a succinct two-line rationale that encapsulates the key security features that affirm its validity. This process is crucial for the accurate differentiation between genuine and counterfeit currency, which is essential to the integrity of financial dealings.User Input:"),
                glm.Part(inline_data=glm.Blob(mime_type='image/jpeg', data=compressed_bytes)),
            ],
        ),
        stream=True
    )


    # Resolve the response
    response.resolve()
        
    return jsonify({'extracted_text': response.text})


