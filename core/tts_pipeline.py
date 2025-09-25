import os
import pyttsx3

# Basic TextProcessor placeholder
# Replace this with your actual text_processor.py if needed
class TextProcessor:
    supported_formats = ['txt', 'pdf', 'docx']

    def process_text(self, text):
        return text.strip()

    def process_document(self, file_content, filename=None):
        if isinstance(file_content, bytes):
            try:
                file_content = file_content.decode('utf-8')
            except:
                return "Error: Could not decode file content"
        return file_content.strip()


class TTSPipeline:
    def __init__(self):
        self.doc_processor = TextProcessor()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

    def _select_voice(self, voice_gender="male"):
        gender = voice_gender.lower()
        selected_voice = None
        for voice in self.voices:
            name_lower = voice.name.lower()
            if gender == "female" and ("female" in name_lower or "zira" in name_lower):
                selected_voice = voice.id
                break
            elif gender == "male" and ("male" in name_lower or "david" in name_lower):
                selected_voice = voice.id
                break
        if not selected_voice:
            selected_voice = self.voices[0].id
        self.engine.setProperty('voice', selected_voice)

    def preprocess_text(self, text):
        return self.doc_processor.process_text(text)

    def generate_speech(self, text, output_path, voice_gender="male"):
        try:
            processed_text = self.preprocess_text(text)
            self._select_voice(voice_gender)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            self.engine.save_to_file(processed_text, output_path)
            self.engine.runAndWait()

            if os.path.exists(output_path):
                return output_path
            else:
                return None
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

    def get_available_voices(self):
        male = []
        female = []
        for v in self.voices:
            name_lower = v.name.lower()
            voice_info = {"id": v.id, "name": v.name}
            if "female" in name_lower or "zira" in name_lower:
                female.append(voice_info)
            elif "male" in name_lower or "david" in name_lower:
                male.append(voice_info)
        return {"male": male, "female": female}

    def get_model_info(self):
        info = {
            "loaded_models": ["pyttsx3 TTS Engine"],
            "supported_languages": ["English"],
            "model_details": {"english": {"model_name": "pyttsx3 default", "type": "offline"}},
            "current_voice_gender": "male",
        }
        return info
