#dev Mueid Mursalin Rifat 
from flask import Flask, request, Response, jsonify, send_file
import requests
import uuid
import time
import os

app = Flask(__name__)

MAGIC_URL = "https://ai-api.magicstudio.com/api/ai-art-generator"

# ⚠️ This client_id
CLIENT_ID = "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o"

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "ShadowX-MagicStudio is running"}), 200

@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt", "watercolour")

    # --- Browser-like headers  ---
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Safari/537.36"
        ),
        "origin": "https://magicstudio.com",
        "referer": "https://magicstudio.com/ai-art-generator/",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    # --- TRUE form-data ---
    files = {
        "prompt": (None, prompt),
        "output_format": (None, "bytes"),
        "user_profile_id": (None, "null"),
        "anonymous_user_id": (None, str(uuid.uuid4())),
        "request_timestamp": (None, str(time.time())),
        "user_is_subscribed": (None, "false"),
        "client_id": (None, CLIENT_ID),
    }

    try:
        r = requests.post(
            MAGIC_URL,
            headers=headers,
            files=files,
            timeout=60
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # --- Success: return image directly ---
    if r.headers.get("content-type", "").startswith("image"):
        return Response(r.content, mimetype=r.headers["content-type"])

    # --- Error or JSON response ---
    return Response(r.text, status=r.status_code)

#End Dev Mueid Mursalin Rifat
if __name__ == "__main__":
    app.run(debug=True)
