# core/tts_pipeline.py
import os
import pyttsx3
from core.text_processor import TextProcessor

class TTSPipeline:
    def __init__(self):
        self.doc_processor = TextProcessor()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

    def _select_voice(self, voice_gender="male"):
        voice_gender = (voice_gender or "male").lower()
        selected_voice = None
        for voice in self.voices:
            vname = voice.name.lower()
            if voice_gender == "female" and ("female" in vname or "zira" in vname):
                selected_voice = voice.id
                break
            elif voice_gender == "male" and ("male" in vname or "david" in vname):
                selected_voice = voice.id
                break
        if not selected_voice:
            selected_voice = self.voices[0].id
        self.engine.setProperty('voice', selected_voice)

    def preprocess_text(self, text):
        return self.doc_processor.process_text(text)

    # ✅ Correct method signature: voice_gender, not voice
    def generate_speech(self, text, output_path, voice_gender="male"):
        try:
            processed_text = self.preprocess_text(text)
            self._select_voice(voice_gender)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            self.engine.save_to_file(processed_text, output_path)
            self.engine.runAndWait()
            return output_path if os.path.exists(output_path) else None
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None

    def generate_speech_from_document(self, file_path, output_path, voice_gender="male"):
        try:
            text = self.doc_processor.process_document(file_path)
            return self.generate_speech(text, output_path, voice_gender)
        except Exception as e:
            print(f"Error generating speech from document: {e}")
            return None

    def get_model_info(self):
        return {
            "loaded_models": ["pyttsx3 TTS Engine"],
            "supported_languages": ["English"],
            "model_details": {"english": {"model_name": "pyttsx3 default", "type": "offline"}}
        }

    def get_available_voices(self):
        voices_info = {"male": [], "female": []}
        for v in self.voices:
            name_lower = v.name.lower()
            if "male" in name_lower or "david" in name_lower:
                voices_info["male"].append({"id": v.id, "name": v.name})
            elif "female" in name_lower or "zira" in name_lower:
                voices_info["female"].append({"id": v.id, "name": v.name})
        return voices_info
