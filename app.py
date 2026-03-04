from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- PASTE YOUR TOKEN HERE ---
HF_API_KEY = "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"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

TEXT_API_URL = "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/umm-maybe/AI-image-detector"

@app.route('/detect-text', methods=['POST'])
def detect_text():
    data = request.json
    payload = {"inputs": data.get('text', '')}
    response = requests.post(TEXT_API_URL, headers=HEADERS, json=payload)
    return jsonify(response.json())

@app.route('/detect-image', methods=['POST'])
def detect_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image found"}), 400
    
    file = request.files['image'].read()
    response = requests.post(IMAGE_API_URL, headers=HEADERS, data=file)
    return jsonify(response.json())

if __name__ == '__main__':
    # Runs on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)