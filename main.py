from flask import Flask, request, jsonify, send_file
#from PIL import Image
import os
import numpy as np
import tempfile

from vertexai import generative_models


from vision import generate_text
from voice import text_to_voice

app = Flask(__name__)


@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    try:
        image_bytes = file.read()
        result = generate_text(image_bytes)


        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/health')
def health():
    return 'Bharat'
    



@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    if not text:
        return {"error": "No text provided"}, 400

    try:
        # tts = gTTS(text=text, lang='en')
        tts= text_to_voice(text)
        # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        # tts.save(temp_file.name)

        # temp_file.write(tts)
        # temp_file.close()  # Must close before sending file to ensure all data is written

        file_path= os.path.join(os.getcwd(), "backend/output.mp3")


        # return send_file(temp_file.name, as_attachment=True, attachment_filename='speech.mp3', mimetype='audio/mp3')
        return send_file(file_path, as_attachment=True, mimetype='audio/mp3')
    except Exception as e:
        return {"error": str(e)}, 500



if __name__ == '__main__':
    app.run(debug=True)
