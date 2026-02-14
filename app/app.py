import traceback
from flask import Flask, request, jsonify,g, send_from_directory
from flask_cors import CORS, cross_origin

from excel_extract import process_text_pipeline

app = Flask(__name__)
CORS(app)  # เปิดการเชื่อมต่อจากทุกโดเมน

@app.route("/api/extract_word", methods=["POST"])
def extract_word():
    try:
        data = request.get_json()
        text = data.get("text")

        res = process_text_pipeline(text)
        return jsonify({"data" : res, "success" :True}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error" : str(e), "success" :False}), 500