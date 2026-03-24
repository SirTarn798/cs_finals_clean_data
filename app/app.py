import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

from excel_extract import process_text_pipeline
from ner_model import predict, extract_entities

app = Flask(__name__)
CORS(app)

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

@app.route("/api/predict", methods=["POST"])
def predict_endpoint():
    try:
        data = request.get_json()
        text = data.get("text")
        if not text:
            return jsonify({"error": "No text provided", "success": False}), 400

        predictions, tokens = predict(text)
        return jsonify({"predictions": predictions, "tokens": tokens, "success": True}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "success": False}), 500

@app.route("/api/extract_entities", methods=["POST"])
def extract_entities_endpoint():
    try:
        data = request.get_json()
        predictions = data.get("predictions")
        if not predictions:
            return jsonify({"error": "No predictions provided", "success": False}), 400

        entities = extract_entities(predictions)
        return jsonify({"entities": entities, "success": True}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "success": False}), 500

@app.route("/api/ner", methods=["POST"])
def ner_endpoint():
    """Combined endpoint: text -> entities in one call"""
    try:
        data = request.get_json()
        text = data.get("text")
        if not text:
            return jsonify({"error": "No text provided", "success": False}), 400

        predictions, tokens = predict(text)
        entities = extract_entities(predictions)
        return jsonify({
            "predictions": predictions,
            "tokens": tokens,
            "entities": entities,
            "success": True
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "success": False}), 500
