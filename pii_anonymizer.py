
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngineProvider
from typing import Tuple, List, Dict
from language_detection import LanguageDetection

class PiiAnonymizer:
    @staticmethod
    def anonymize(text: str) -> Tuple[str, str, str, List[Dict]]:
        lang_detect = LanguageDetection()
        detected_lang = lang_detect.detect_lang(text)

        provider = AnalyzerEngineProvider(analyzer_engine_conf_file="analyzer_config.yml")
        analyzer = provider.create_engine()

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
        anonymized_result = anonymizer.anonymize(text, analyzer_results)

        for entity, anonymized in zip(replaced_entities, anonymized_result.items):
            entity["replacement_text"] = anonymized.text

        return text, anonymized_result.text, detected_lang, replaced_entities
