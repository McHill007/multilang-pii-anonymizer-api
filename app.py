
from flask import Flask, request, jsonify
from pii_anonymizer import PiiAnonymizer

app = Flask(__name__)

@app.route("/anonymize", methods=["POST"])
def anonymize():
    try:
        import os
        print("Working dir:", os.getcwd())
        print("YAML exists:", os.path.exists("analyzer_config.yml"))

        data = request.get_json(force=True)
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        from pii_anonymizer import PiiAnonymizer
        original, anonymized, lang, entities = PiiAnonymizer.anonymize(text)

        return jsonify({
            "language": lang,
            "original": original,
            "anonymized": anonymized,
            "entities": entities
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
