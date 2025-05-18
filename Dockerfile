
FROM python:3.10-slim

WORKDIR /app

COPY app.py pii_anonymizer.py language_detection.py analyzer_config.yml requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_lg && \
    python -m spacy download nb_core_news_lg && \
    python -m spacy download es_core_news_lg && \
    python -m spacy download de_core_news_lg && \
    python -m spacy download it_core_news_lg

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

