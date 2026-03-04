from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# --- PASTE YOUR ACTUAL TOKEN HERE ---
HF_API_KEY = "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" 
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

TEXT_API_URL = "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/umm-maybe/AI-image-detector"

def query_model(url, data, is_binary=False):
    for _ in range(3):
        if is_binary:
            response = requests.post(url, headers=HEADERS, data=data)
        else:
            response = requests.post(url, headers=HEADERS, json=data)
        
        try:
            result = response.json()
        except:
            return {"error": "Invalid response from AI"}

        if isinstance(result, dict) and "estimated_time" in result:
            time.sleep(10) # Wait if model is loading
            continue
        return result
    return {"error": "Model took too long to load"}

@app.route('/')
def home():
    return "AI Detector Server is Live!"

@app.route('/detect-text', methods=['POST'])
def detect_text():
    data = request.json
    result = query_model(TEXT_API_URL, {"inputs": data.get('text', '')})
    return jsonify(result)

@app.route('/detect-image', methods=['POST'])
def detect_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image found"}), 400
    file_data = request.files['image'].read()
    result = query_model(IMAGE_API_URL, file_data, is_binary=True)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
