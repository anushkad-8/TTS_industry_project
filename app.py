import streamlit as st
import os
from core.tts_pipeline import TTSPipeline

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Advanced TTS System",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Custom CSS -------------------
st.markdown("""
<style>
    .main-header { font-size: 3rem; color: #1E88E5; text-align: center; margin-bottom: 2rem; }
    .sub-header { font-size: 1.5rem; color: #424242; margin-bottom: 1rem; }
    .success-message { padding: 1rem; background-color: #E8F5E8; border-radius: 0.5rem; border-left: 5px solid #4CAF50; }
    .error-message { padding: 1rem; background-color: #FFEBEE; border-radius: 0.5rem; border-left: 5px solid #F44336; }
    .voice-info { padding: 0.5rem; background-color: #E3F2FD; border-radius: 0.5rem; border-left: 3px solid #2196F3; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ------------------- Session State -------------------
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
    st.session_state.initialization_status = "Not Started"

# ------------------- Initialize Pipeline -------------------
@st.cache_resource
def initialize_pipeline():
    try:
        pipeline = TTSPipeline()
        return pipeline, "Success"
    except Exception as e:
        return None, f"Error: {str(e)}"

if st.session_state.pipeline is None:
    with st.spinner("🚀 Initializing TTS System... This may take a few minutes on first run."):
        pipeline, status = initialize_pipeline()
        st.session_state.pipeline = pipeline
        st.session_state.initialization_status = status

pipeline = st.session_state.pipeline
if "Error" in st.session_state.initialization_status:
    st.error(f"Failed to initialize TTS system: {st.session_state.initialization_status}")
    st.stop()

# ------------------- Sidebar -------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a feature:", ["🏠 Home", "📝 Text to Speech", "📄 Document to Speech", "ℹ️ System Info"])

# ------------------- Header -------------------
st.markdown('<h1 class="main-header">🎵 Advanced Text-to-Speech System</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#666;font-size:1.2rem;">Convert text & documents to high-quality speech with male & female voices!</p>', unsafe_allow_html=True)

# ------------------- Home Page -------------------
if page == "🏠 Home":
    st.markdown('<h2 class="sub-header">Welcome!</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎯 Features")
        st.write("✅ Text to Speech")
        st.write("✅ Document to Speech")
        st.write("✅ Male & Female Voices")
        st.write("✅ Preview & Download")
        st.write("✅ High Quality WAV Output")

    with col2:
        st.markdown("### 📁 Supported Files")
        st.write("📝 TXT")
        st.write("📄 PDF")
        st.write("📄 DOCX")
        st.write("⌨️ Direct Text Input")

    with col3:
        st.markdown("### 🔧 System Status")
        if pipeline:
            st.success("✅ TTS Engine: Ready")
            st.success("✅ Text Processor: Ready")
            st.success("✅ Document Processor: Ready")
            try:
                voices_info = pipeline.get_available_voices()
                male_count = len(voices_info.get('male', []))
                female_count = len(voices_info.get('female', []))
                st.info(f"🎤 Voices Available:\n• Male: {male_count}\n• Female: {female_count}")
            except:
                st.info("🎤 Voice system ready")
        else:
            st.error("❌ System Not Initialized")

    st.markdown("---")
    st.markdown("### 🎮 Quick Demo")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Demo Male Voice"):
            demo_text = "Hello! This is a demo of the male voice."
            out = "outputs/demo_male.wav"
            pipeline.generate_speech(demo_text, out, voice_gender="male")
            with open(out, "rb") as f:
                st.audio(f.read(), format="audio/wav")
    with col2:
        if st.button("Demo Female Voice"):
            demo_text = "Hello! This is a demo of the female voice."
            out = "outputs/demo_female.wav"
            pipeline.generate_speech(demo_text, out, voice_gender="female")
            with open(out, "rb") as f:
                st.audio(f.read(), format="audio/wav")

# ------------------- Text-to-Speech Page -------------------
elif page == "📝 Text to Speech":
    st.markdown('<h2 class="sub-header">Text to Speech</h2>', unsafe_allow_html=True)

    voice_gender = st.selectbox("Select Voice Gender:", ["male", "female"])

    text_input = st.text_area("Enter text to convert:", height=200)

    output_filename = st.text_input("Output filename:", value=f"speech_{voice_gender}.wav")

    if st.button("Generate Speech"):
        if not text_input.strip():
            st.error("Enter some text!")
        else:
            out_path = os.path.join("outputs", output_filename)
            result = pipeline.generate_speech(text_input, out_path, voice_gender=voice_gender)
            if result and os.path.exists(result):
                st.success(f"{voice_gender.title()} speech generated!")
                with open(result, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/wav")
                    st.download_button(f"Download {voice_gender.title()} Audio", audio_bytes, file_name=output_filename, mime="audio/wav")
            else:
                st.error("Failed to generate speech.")

# ------------------- Document-to-Speech Page -------------------
elif page == "📄 Document to Speech":
    st.markdown('<h2 class="sub-header">Document to Speech</h2>', unsafe_allow_html=True)

    doc_voice_gender = st.selectbox("Select Voice Gender:", ["male", "female"], key="doc_gender")
    uploaded_file = st.file_uploader("Upload Document (txt, pdf, docx):", type=["txt","pdf","docx"])

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        try:
            file_content = uploaded_file.read()
            extracted_text = pipeline.doc_processor.process_document(file_content, uploaded_file.name)
            if extracted_text.startswith("Error:"):
                st.error(extracted_text)
            else:
                st.markdown("### Preview Text")
                preview_text = extracted_text[:500]+"..." if len(extracted_text)>500 else extracted_text
                st.text_area("Preview:", preview_text, height=150, disabled=True)

                word_count = len(extracted_text.split())
                char_count = len(extracted_text)
                est_duration = word_count/150*60
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Words", word_count)
                col2.metric("Characters", char_count)
                col3.metric("Est. Duration", f"{est_duration:.1f}s")
                col4.metric("Voice", doc_voice_gender.title())

                output_filename = st.text_input("Output filename:", value=f"doc_{uploaded_file.name.split('.')[0]}_{doc_voice_gender}.wav")

                if st.button("Convert Document to Speech"):
                    out_path = os.path.join("outputs", output_filename)
                    result = pipeline.generate_speech(extracted_text, out_path, voice_gender=doc_voice_gender)
                    if result and os.path.exists(result):
                        st.success("Document converted to speech!")
                        with open(result,"rb") as f:
                            audio_bytes = f.read()
                            st.audio(audio_bytes, format="audio/wav")
                            st.download_button(f"Download {doc_voice_gender.title()} Audio", audio_bytes, file_name=output_filename, mime="audio/wav")
                    else:
                        st.error("Conversion failed.")
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")

# ------------------- System Info Page -------------------
elif page == "ℹ️ System Info":
    st.markdown('<h2 class="sub-header">System Info</h2>', unsafe_allow_html=True)
    model_info = pipeline.get_model_info()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔧 System Status")
        st.success("✅ TTS Pipeline: Active")
        st.success("✅ Text Processor: Ready")
        st.success("✅ Document Processor: Ready")
        st.info(f"Loaded Models: {len(model_info['loaded_models'])}")
        st.info(f"Current Voice: {model_info.get('current_voice_gender','Unknown').title()}")

    with col2:
        st.markdown("### 📋 Supported Features")
        st.write("🎯 Text to Speech")
        st.write("👨 Male Voice Support")
        st.write("👩 Female Voice Support")
        st.write("📄 Document Processing")
        st.write("🔤 Text Preprocessing")
        st.write("📝 Multiple File Formats")

    st.markdown("### 🎤 Voice System Details")
    voices_info = pipeline.get_available_voices()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👨 Male Voices")
        male_voices = voices_info.get('male',[])
        st.write("• " + "\n• ".join([v['name'] for v in male_voices[:5]]) if male_voices else "No male voices")
    with col2:
        st.markdown("#### 👩 Female Voices")
        female_voices = voices_info.get('female',[])
        st.write("• " + "\n• ".join([v['name'] for v in female_voices[:5]]) if female_voices else "No female voices")

    st.markdown("### 🤖 Model Details")
    for lang, details in model_info['model_details'].items():
        st.write(f"**{lang.title()}:**")
        for k,v in details.items():
            st.write(f"• {k}: {v}")

    st.markdown("### ⚡ Performance Tips")
    st.info("""
    • Male voices: deeper tones, good for narration
    • Female voices: clearer tones, good for education/content
    • Short texts (<500 chars) process faster
    • PDF extraction may be slower on scanned/complex docs
    • First-time load may take 1–2 mins
    """)

# ------------------- Footer -------------------
st.markdown("---")
st.markdown("*Advanced TTS System - High Quality Male & Female Voice Support*")
st.markdown("*Built with Streamlit & pyttsx3*")
