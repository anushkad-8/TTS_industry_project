import os
import pyttsx3
from core.text_processor import TextProcessor

class TTSPipeline:
    def __init__(self):
        self.doc_processor = TextProcessor()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

    def _select_voice(self, gender="male"):
        """Select a voice based on gender if available"""
        gender = gender.lower()
        selected_voice = None
        for voice in self.voices:
            if gender == "female" and ("female" in voice.name.lower() or "zira" in voice.name.lower()):
                selected_voice = voice.id
                break
            elif gender == "male" and ("male" in voice.name.lower() or "david" in voice.name.lower()):
                selected_voice = voice.id
                break
        if not selected_voice:
            # fallback to default voice
            selected_voice = self.voices[0].id
        self.engine.setProperty('voice', selected_voice)

    def preprocess_text(self, text):
        return self.doc_processor.process_text(text)

    def generate_speech(self, text, output_path, voice="male"):
        try:
            processed_text = self.preprocess_text(text)
            self._select_voice(voice)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Generate speech and save
            self.engine.save_to_file(processed_text, output_path)
            self.engine.runAndWait()

            if os.path.exists(output_path):
                return output_path
            else:
                return None
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None

    def generate_speech_from_document(self, file_path, output_path, voice="male"):
        try:
            text = self.doc_processor.process_document(file_path)
            return self.generate_speech(text, output_path, voice)
        except Exception as e:
            print(f"Error generating speech from document: {e}")
            return None

    def get_model_info(self):
        info = {
            "loaded_models": ["pyttsx3 TTS Engine"],
            "supported_languages": ["English"],
            "model_details": {"english": {"model_name": "pyttsx3 default", "type": "offline"}}
        }
        return info
