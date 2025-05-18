import os
import yaml

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer import AnalyzerEngineProvider
from presidio_analyzer import PatternRecognizer, Pattern

from typing import Tuple, List, Dict
from language_detection import LanguageDetection

def load_custom_recognizers_from_yaml(path: str, detected_lang: str):
    if not os.path.isfile(path):
        return []

    recognizers = []
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for entry in data.get("recognizers", []):
        pattern = Pattern(entry["name"], entry["pattern"], float(entry.get("score", 0.5)))
        recognizer = PatternRecognizer(
            supported_entity=entry["entity_type"],
            name=entry["name"],
            patterns=[pattern],
            supported_language=detected_lang
        )
        recognizers.append(recognizer)

    return recognizers

class PiiAnonymizer:
    @staticmethod
    def anonymize(text: str, debug: bool = False) -> Tuple[str, str, str, List[Dict]]:
        lang_detect = LanguageDetection()
        detected_lang = lang_detect.detect_lang(text)

        provider = AnalyzerEngineProvider(analyzer_engine_conf_file="analyzer_config.yml")
        analyzer = provider.create_engine()

        for r in load_custom_recognizers_from_yaml("recognizers.yaml", detected_lang):
            analyzer.registry.add_recognizer(r)


        analyzer_results = analyzer.analyze(text=text, language=detected_lang)

        replaced_entities = []
        for result in analyzer_results:
            replaced_entities.append({
                "entity_type": result.entity_type,
                "original_text": text[result.start:result.end],
                "start": result.start,
                "end": result.end
            })

        anonymizer = AnonymizerEngine()

        operator_config = {
            "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL_ADDRESS>"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE_NUMBER>"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<CREDIT_CARD>"}),
            "DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"})
        }

        for r in load_custom_recognizers_from_yaml("recognizers.yaml", detected_lang):
            entity = r.supported_entities[0]
            if entity not in operator_config:
                operator_config[entity] = OperatorConfig("replace", {"new_value": f"<{entity}>"})
            analyzer.registry.add_recognizer(r)
        
        anonymized_result = anonymizer.anonymize(text, analyzer_results, operators=operator_config)

        for entity, anonymized in zip(replaced_entities, anonymized_result.items):
            entity["replacement_text"] = anonymized.text

        if debug:
            print(f"[DEBUG] Detected language: {detected_lang}")
            print(f"[DEBUG] Registered recognizers:")
            for r in analyzer.registry.recognizers:
                print(f"  - {r.name} → {r.supported_entities}")
            print("[DEBUG] Analyzer results:")
            for r in analyzer_results:
                print(f"  - {r.entity_type}: '{text[r.start:r.end]}' @ {r.start}-{r.end} (score: {r.score})")

        return text, anonymized_result.text, detected_lang, replaced_entities
