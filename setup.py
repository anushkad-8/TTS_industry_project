#!/usr/bin/env python3
"""
Quick setup script for TTS Project
Run this after installing requirements to verify everything works
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = ["core", "utils", "outputs", "uploads"]
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ - OK")
        else:
            print(f"📝 Creating {directory}/")
            os.makedirs(directory, exist_ok=True)
    
    # Check for __init__.py files
    init_files = ["core/__init__.py", "utils/__init__.py"]
    for init_file in init_files:
        if os.path.exists(init_file):
            print(f"✅ {init_file} - OK")
        else:
            print(f"📝 Creating {init_file}")
            with open(init_file, 'w') as f:
                f.write("# This file makes Python treat the directory as a package\n")

def check_dependencies():
    """Check if key dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    dependencies_status = []
    
    # Check streamlit
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
        dependencies_status.append(True)
    except ImportError:
        print("❌ Streamlit not found")
        dependencies_status.append(False)
    
    # Check pyttsx3
    try:
        import pyttsx3
        print("✅ pyttsx3 (Offline TTS) installed")
        dependencies_status.append(True)
    except ImportError:
        print("⚠️  pyttsx3 not found - offline TTS unavailable")
        dependencies_status.append(False)
    
    # Check gTTS
    try:
        from gtts import gTTS
        print("✅ gTTS (Google TTS) installed")
        dependencies_status.append(True)
    except ImportError:
        print("⚠️  gTTS not found - online TTS unavailable")
        dependencies_status.append(False)
    
    # Check document processing libraries
    try:
        from PyPDF2 import PdfReader
        print("✅ PyPDF2 (PDF processing)")
        dependencies_status.append(True)
    except ImportError:
        print("❌ PyPDF2 not found")
        dependencies_status.append(False)
    
    try:
        import docx
        print("✅ python-docx (Word processing)")
        dependencies_status.append(True)
    except ImportError:
        print("❌ python-docx not found")
        dependencies_status.append(False)
    
    # Check if at least one TTS engine is available
    tts_available = False
    try:
        import pyttsx3
        tts_available = True
    except ImportError:
        pass
    
    try:
        from gtts import gTTS
        tts_available = True
    except ImportError:
        pass
    
    if not tts_available:
        print("❌ No TTS engines available! Install pyttsx3 or gTTS")
        return False
    
    return any(dependencies_status)

def test_basic_imports():
    """Test if our custom modules can be imported"""
    print("\n🔧 Testing module imports...")
    
    try:
        from core.tts_pipeline import TTSPipeline
        print("✅ TTS Pipeline import - OK")
    except ImportError as e:
        print(f"❌ TTS Pipeline import failed: {e}")
        return False
    
    try:
        from utils.text_processor import TextProcessor
        print("✅ Text Processor import - OK")
    except ImportError as e:
        print(f"❌ Text Processor import failed: {e}")
        return False
    
    try:
        from core.document_processor import DocumentProcessor
        print("✅ Document Processor import - OK")
    except ImportError as e:
        print(f"❌ Document Processor import failed: {e}")
        return False
    
    return True

def run_quick_test():
    """Run a very quick functionality test"""
    print("\n⚡ Running quick functionality test...")
    
    try:
        from utils.text_processor import TextProcessor
        
        processor = TextProcessor()
        test_text = "Dr. Smith won't be available, etc."
        result = processor.process_text(test_text)
        
        print(f"📝 Original: {test_text}")
        print(f"📝 Processed: {result}")
        print("✅ Text processing - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def test_tts_engines():
    """Test available TTS engines"""
    print("\n🎵 Testing TTS engines...")
    
    # Test pyttsx3
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"✅ pyttsx3: {len(voices) if voices else 0} voices available")
        engine.stop()
    except Exception as e:
        print(f"⚠️  pyttsx3 test failed: {e}")
    
    # Test gTTS
    try:
        from gtts import gTTS
        # Just test import, don't make actual request
        print("✅ gTTS: Ready (requires internet for actual use)")
    except Exception as e:
        print(f"⚠️  gTTS test failed: {e}")

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Run comprehensive tests:")
    print("   python test_pipeline.py")
    
    print("\n2. Start the web application:")
    print("   streamlit run app.py")
    
    print("\n3. Or test individual components:")
    print("   python core/tts_pipeline.py")
    print("   python utils/text_processor.py")
    
    print("\n💡 TIPS:")
    print("• pyttsx3 works offline with system voices")
    print("• gTTS requires internet but has better quality")
    print("• Audio files will be saved in 'outputs/' directory")
    print("• Check console for detailed error messages if something fails")
    
    print(f"\n📂 Project structure:")
    print("tts_project/")
    print("├── app.py                 (Main web application)")
    print("├── test_pipeline.py       (Comprehensive tests)")
    print("├── core/")
    print("│   ├── tts_pipeline.py    (Main TTS logic)")
    print("│   └── document_processor.py")
    print("├── utils/")
    print("│   └── text_processor.py")
    print("└── outputs/               (Generated audio files)")

def main():
    """Main setup function"""
    print("🚀 TTS PROJECT SETUP")
    print("="*60)
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", lambda: (check_directories(), True)[1]),
        ("Dependencies", check_dependencies),
        ("Module Imports", test_basic_imports),
        ("Quick Test", run_quick_test),
        ("TTS Engines", lambda: (test_tts_engines(), True)[1])
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            all_passed = False
    
    if all_passed:
        print_next_steps()
        return True
    else:
        print("\n⚠️  Some setup checks failed. Please review the messages above.")
        print("💡 Common solutions:")
        print("• Run: pip install -r requirements.txt")
        print("• Check internet connection if using gTTS")
        print("• Ensure Python 3.8+ is being used")
        print("• Make sure all Python files are created correctly")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)