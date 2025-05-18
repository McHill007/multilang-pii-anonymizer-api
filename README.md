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
    restart: unless-stopped
```
---

## 🐳 Use Prebuilt Docker Image

You can also run the PII Anonymizer API directly using the prebuilt image from Docker Hub:

```bash
`docker pull mchill007/pii-anonymizer-api` 
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

## 🧠 Tech Stack

- Python 3.10
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
