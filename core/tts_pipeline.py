import os
import time
import tempfile
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

from utils.text_processor import TextProcessor
from core.document_processor import DocumentProcessor

class TTSPipeline:
    def __init__(self, engine_type="pyttsx3"):
        print("Initializing TTS Pipeline...")
        
        # Initialize text and document processors
        self.text_processor = TextProcessor()
        self.doc_processor = DocumentProcessor()
        
        # Initialize TTS engine
        self.engine_type = engine_type
        self.engine = None
        self.load_models()
        
        print("TTS Pipeline initialized successfully!")
    
    def load_models(self):
        """Load TTS models"""
        try:
            if self.engine_type == "pyttsx3" and PYTTSX3_AVAILABLE:
                print("Loading pyttsx3 TTS engine...")
                self.engine = pyttsx3.init()
                
                # Configure voice settings
                voices = self.engine.getProperty('voices')
                if voices:
                    # Try to find a male voice
                    male_voice = None
                    for voice in voices:
                        if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                            male_voice = voice
                            break
                    
                    if male_voice:
                        self.engine.setProperty('voice', male_voice.id)
                        print(f"Using voice: {male_voice.name}")
                    else:
                        # Use first available voice
                        self.engine.setProperty('voice', voices[0].id)
                        print(f"Using default voice: {voices[0].name}")
                
                # Set speech rate and volume
                self.engine.setProperty('rate', 200)    # Speed of speech
                self.engine.setProperty('volume', 0.9)   # Volume level (0.0 to 1.0)
                
                print("pyttsx3 engine loaded successfully!")
                
            elif self.engine_type == "gtts" and GTTS_AVAILABLE:
                print("Using gTTS (Google Text-to-Speech) engine...")
                self.engine = "gtts"  # We'll use gTTS directly in generation
                print("gTTS engine configured successfully!")
                
            else:
                raise Exception("No compatible TTS engine available")
                
        except Exception as e:
            print(f"Error loading TTS engine: {e}")
            # Try fallback
            try:
                if GTTS_AVAILABLE and self.engine_type != "gtts":
                    print("Falling back to gTTS...")
                    self.engine = "gtts"
                    self.engine_type = "gtts"
                    print("Fallback successful!")
                else:
                    raise Exception("Could not initialize any TTS engine")
            except Exception as e2:
                print(f"Fallback failed: {e2}")
                raise Exception("Could not load any TTS engine")
    
    def preprocess_text(self, text):
        """Preprocess text before TTS"""
        if not text or not isinstance(text, str):
            return ""
        
        # Use text processor
        processed_text = self.text_processor.process_text(text)
        
        # Additional preprocessing for TTS
        # Limit text length for better processing (split if too long)
        max_length = 500  # characters
        if len(processed_text) > max_length:
            # Split into sentences and process in chunks
            sentences = processed_text.split('. ')
            processed_text = '. '.join(sentences[:5])  # Take first 5 sentences
            if not processed_text.endswith('.'):
                processed_text += '.'
        
        return processed_text
    
    def generate_speech(self, text, output_path="output.wav", language="english"):
        """Generate speech from text"""
        try:
            # Preprocess text
            processed_text = self.preprocess_text(text)
            
            if not processed_text:
                raise ValueError("No text to process")
            
            print(f"Generating speech for: {processed_text[:50]}...")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
            
            # Generate speech based on engine type
            if self.engine_type == "pyttsx3":
                # Use pyttsx3 for offline generation
                self.engine.save_to_file(processed_text, output_path)
                self.engine.runAndWait()
                
            elif self.engine_type == "gtts":
                # Use gTTS for online generation
                tts = gTTS(text=processed_text, lang='en', slow=False)
                tts.save(output_path)
            
            # Verify file was created
            if os.path.exists(output_path):
                print(f"Speech generated successfully: {output_path}")
                return output_path
            else:
                print("Error: Audio file was not created")
                return None
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None
    
    def generate_speech_from_document(self, file_path_or_bytes, filename=None, output_path="document_output.wav"):
        """Generate speech from document"""
        try:
            # Extract text from document
            extracted_text = self.doc_processor.process_document(file_path_or_bytes, filename)
            
            if extracted_text.startswith("Error:"):
                print(extracted_text)
                return None
            
            # Generate speech
            return self.generate_speech(extracted_text, output_path)
            
        except Exception as e:
            print(f"Error processing document: {e}")
            return None
    
    def batch_process_texts(self, texts, output_dir="outputs"):
        """Process multiple texts"""
        results = []
        os.makedirs(output_dir, exist_ok=True)
        
        for i, text in enumerate(texts):
            output_path = os.path.join(output_dir, f"batch_output_{i+1}.wav")
            result = self.generate_speech(text, output_path)
            results.append(result)
            
        return results
    
    def get_model_info(self):
        """Get information about loaded models"""
        info = {
            'loaded_models': [self.engine_type],
            'supported_languages': ['english'],
            'model_details': {}
        }
        
        if self.engine_type == "pyttsx3" and self.engine:
            voices = self.engine.getProperty('voices')
            current_voice = self.engine.getProperty('voice')
            
            info['model_details']['english'] = {
                'engine': 'pyttsx3 (Offline)',
                'current_voice': current_voice,
                'available_voices': len(voices) if voices else 0
            }
        elif self.engine_type == "gtts":
            info['model_details']['english'] = {
                'engine': 'gTTS (Google Text-to-Speech)',
                'language': 'en',
                'requires_internet': True
            }
        
        return info

# Test the pipeline
if __name__ == "__main__":
    try:
        # Test both engines if available
        engines_to_test = []
        if PYTTSX3_AVAILABLE:
            engines_to_test.append("pyttsx3")
        if GTTS_AVAILABLE:
            engines_to_test.append("gtts")
        
        if not engines_to_test:
            print("No TTS engines available. Please install pyttsx3 or gTTS.")
            exit(1)
        
        for engine_type in engines_to_test:
            print(f"\n{'='*50}")
            print(f"Testing {engine_type.upper()} engine")
            print('='*50)
            
            # Initialize pipeline
            pipeline = TTSPipeline(engine_type=engine_type)
            
            # Test basic text generation
            print(f"\nTesting basic text generation with {engine_type}...")
            test_text = "Hello! This is a test of our text-to-speech pipeline using " + engine_type
            result = pipeline.generate_speech(test_text, f"test_output_{engine_type}.wav")
            
            if result:
                print(f"Success! Audio saved to: {result}")
            else:
                print("Failed to generate speech")
            
            # Test model info
            print(f"\nModel Information for {engine_type}:")
            info = pipeline.get_model_info()
            for key, value in info.items():
                print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Test failed: {e}")