# PII Anonymizer API

A multilingual Flask-based API for detecting and anonymizing Personally Identifiable Information (PII) using Microsoft Presidio.

Supports English, Norwegian, Spanish, German, and Italian.

---

## 🚀 Features

- 🔍 Automatic language detection using spaCy and spacy-langdetect
- 🛡️ PII detection for email addresses, phone numbers, credit card numbers, and names
- 🌐 Multilingual support (en, no, es, de, it)
- ⚙️ Configurable recognizers and NLP models via YAML
- 🐳 Easy deployment with Docker and Docker Compose

---

## 📦 Example API Usage

### Endpoint

POST /anonymize  
Content-Type: application/json

### Request Body
```json
{
  "text": "My name is John Smith. My email is john@example.com."
}
```

### Response
```json
{
  "language": "en",
  "original": "My name is John Smith. My email is john@example.com.",
  "anonymized": "My name is <PERSON>. My email is <EMAIL_ADDRESS>.",
  "entities": [
    {
      "entity_type": "PERSON",
      "original_text": "John Smith",
      "replacement_text": "<PERSON>"
    },
    {
      "entity_type": "EMAIL_ADDRESS",
      "original_text": "john@example.com",
      "replacement_text": "<EMAIL_ADDRESS>"
    }
  ]
}
```

---

## 🛠️ Run with Docker
```bash
docker build -t pii-anonymizer-api .  
docker run -p 5000:5000 pii-anonymizer-api
```
### Or with Docker Compose
```yaml
services:  
  pii-anonymizer-api:  
    build:  
      context: .  
    ports:  
      - "5000:5000"  
    #Optional load custom recognizers
    #volumes:
    #  - ./recognizers.yaml:/app/recognizers.yaml:ro
    restart: unless-stopped
```
---

## 🐳 Use Prebuilt Docker Image

You can also run the PII Anonymizer API directly using the prebuilt image from Docker Hub:

```bash
docker pull mchill007/pii-anonymizer-api
```
### Example `docker-compose.yml`

```yaml
services:
  pii-anonymizer-api:
    image: mchill007/pii-anonymizer-api:latest
    ports:
      - "5000:5000"
    restart: unless-stopped
 
```
This will start the API at `http://localhost:5000/anonymize` without requiring you to build the image locally.

## 🔧 Custom Regex Recognizers via `recognizers.yaml`

You can define your own PII patterns (e.g., order numbers, internal IDs) using a simple YAML file.  
This allows you to extend or replace recognizers without modifying any code.

### Example: `recognizers.yaml`

```yaml  
-   name: AmazonOrderRecognizer  
    entity_type: AMAZON_ORDER  
    pattern: "\(?\d{3}-\d{7}-\d{7}\)?"  
    score: 1.0
```    

### How it's done

The app will automatically load this file at runtime and register the recognizers dynamically based on the detected language of each request.

Place the file in the root directory (or configure the path in your code):

```python
for recognizer in load_custom_recognizers_from_yaml("recognizers.yaml", detected_lang):  
	analyzer.registry.add_recognizer(recognizer)
```
This allows you to:

-   Keep sensitive patterns out of source code
-   Maintain environment-specific recognizers (e.g., dev vs. prod)    
-   Easily extend functionality without redeploying

---

## 🧠 Tech Stack

- Python 3.12
- Flask
- Microsoft Presidio (presidio-analyzer, presidio-anonymizer)
- spaCy + spacy-langdetect
- Docker

---

## 📁 Project Structure
````bash
.
├── app.py                  - Flask API  
├── pii_anonymizer.py       - PII processing logic using Presidio  
├── language_detection.py   - spaCy-based language detection  
├── analyzer_config.yml     - Presidio configuration for models/recognizers  
├── Dockerfile  
├── requirements.txt  
└── README.md
````
---


## 📄 License

This project is licensed under the Apache 2.0 License.  
It uses Microsoft Presidio, also licensed under Apache 2.0.

---

## ✨ Credits

Built with ❤️ using Microsoft Presidio, spaCy, and Flask.
