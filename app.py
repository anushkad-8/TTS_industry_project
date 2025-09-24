import streamlit as st
import os
import tempfile
import time
from core.tts_pipeline import TTSPipeline

# Page configuration
st.set_page_config(
    page_title="Advanced TTS System",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #E8F5E8;
        border-radius: 0.5rem;
        border-left: 5px solid #4CAF50;
    }
    .error-message {
        padding: 1rem;
        background-color: #FFEBEE;
        border-radius: 0.5rem;
        border-left: 5px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
    st.session_state.initialization_status = "Not Started"

# Header
st.markdown('<h1 class="main-header">🎵 Advanced Text-to-Speech System</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a feature:", 
                           ["🏠 Home", "📝 Text to Speech", "📄 Document to Speech", "ℹ️ System Info"])

# Initialize Pipeline Function
@st.cache_resource
def initialize_pipeline():
    """Initialize TTS pipeline with caching"""
    try:
        pipeline = TTSPipeline()
        return pipeline, "Success"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Initialize pipeline if not done
if st.session_state.pipeline is None:
    with st.spinner("🚀 Initializing TTS System... This may take a few minutes on first run."):
        pipeline, status = initialize_pipeline()
        st.session_state.pipeline = pipeline
        st.session_state.initialization_status = status

# Check initialization status
if "Error" in st.session_state.initialization_status:
    st.error(f"Failed to initialize TTS system: {st.session_state.initialization_status}")
    st.info("Please check your internet connection and try refreshing the page.")
    st.stop()

pipeline = st.session_state.pipeline

# Home Page
if page == "🏠 Home":
    st.markdown('<h2 class="sub-header">Welcome to Advanced TTS System</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Features")
        st.write("✅ Text to Speech")
        st.write("✅ Document Processing")
        st.write("✅ Multiple Formats")
        st.write("✅ High Quality Audio")
    
    with col2:
        st.markdown("### 📁 Supported Files")
        st.write("📄 PDF Documents")
        st.write("📝 Word Documents")
        st.write("📋 Text Files")
        st.write("⌨️ Direct Text Input")
    
    with col3:
        st.markdown("### 🔧 System Status")
        if pipeline:
            st.success("✅ TTS Engine: Ready")
            st.success("✅ Text Processor: Ready")
            st.success("✅ Document Parser: Ready")
        else:
            st.error("❌ System Not Initialized")
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate to different features!")

# Text to Speech Page
elif page == "📝 Text to Speech":
    st.markdown('<h2 class="sub-header">Text to Speech Conversion</h2>', unsafe_allow_html=True)
    
    # Text input section
    st.markdown("### Enter your text:")
    text_input = st.text_area(
        "Type or paste your text here:",
        value="Welcome to our advanced text-to-speech system! This technology can convert written text into natural-sounding speech.",
        height=200,
        help="Enter the text you want to convert to speech"
    )
    
    # Options
    col1, col2 = st.columns(2)
    with col1:
        output_filename = st.text_input("Output filename:", value="speech_output.wav")
    with col2:
        if st.button("📊 Analyze Text"):
            if text_input:
                word_count = len(text_input.split())
                char_count = len(text_input)
                est_duration = word_count / 150 * 60  # Rough estimate: 150 words per minute
                
                st.info(f"📈 Text Analysis:\n\n"
                       f"• Words: {word_count}\n\n"
                       f"• Characters: {char_count}\n\n"
                       f"• Estimated Duration: {est_duration:.1f} seconds")
    
    # Generate speech button
    if st.button("🎵 Generate Speech", type="primary"):
        if not text_input.strip():
            st.error("Please enter some text to convert!")
        else:
            try:
                with st.spinner("🎧 Generating audio... Please wait."):
                    # Create output path
                    output_path = os.path.join("outputs", output_filename)
                    
                    # Generate speech
                    result = pipeline.generate_speech(text_input, output_path)
                    
                    if result and os.path.exists(result):
                        st.success("🎉 Speech generated successfully!")
                        
                        # Display audio player
                        with open(result, 'rb') as audio_file:
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/wav')
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Audio",
                            data=audio_bytes,
                            file_name=output_filename,
                            mime="audio/wav"
                        )
                        
                        # Show file info
                        file_size = os.path.getsize(result) / 1024  # KB
                        st.info(f"📁 File saved: {output_filename} ({file_size:.1f} KB)")
                        
                    else:
                        st.error("❌ Failed to generate speech. Please try again.")
                        
            except Exception as e:
                st.error(f"❌ Error generating speech: {str(e)}")

# Document to Speech Page
elif page == "📄 Document to Speech":
    st.markdown('<h2 class="sub-header">Document to Speech Conversion</h2>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### Upload your document:")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'pdf', 'docx'],
        help="Supported formats: TXT, PDF, DOCX"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"📁 File uploaded: {uploaded_file.name}")
        st.info(f"📊 File size: {uploaded_file.size / 1024:.1f} KB")
        
        # Extract and preview text
        try:
            with st.spinner("📖 Extracting text from document..."):
                # Get file content
                file_content = uploaded_file.read()
                extracted_text = pipeline.doc_processor.process_document(file_content, uploaded_file.name)
            
            if extracted_text and not extracted_text.startswith("Error:"):
                # Preview text
                st.markdown("### 📖 Document Preview:")
                preview_text = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
                st.text_area("Extracted text preview:", preview_text, height=150, disabled=True)
                
                # Statistics
                word_count = len(extracted_text.split())
                char_count = len(extracted_text)
                est_duration = word_count / 150 * 60
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Words", word_count)
                with col2:
                    st.metric("Characters", char_count)
                with col3:
                    st.metric("Est. Duration", f"{est_duration:.1f}s")
                
                # Generate speech
                output_filename = st.text_input("Output filename:", value=f"doc_{uploaded_file.name.split('.')[0]}.wav")
                
                if st.button("🎵 Convert Document to Speech", type="primary"):
                    try:
                        with st.spinner("🎧 Converting document to speech... Please wait."):
                            output_path = os.path.join("outputs", output_filename)
                            result = pipeline.generate_speech(extracted_text, output_path)
                            
                            if result and os.path.exists(result):
                                st.success("🎉 Document converted successfully!")
                                
                                # Display audio player
                                with open(result, 'rb') as audio_file:
                                    audio_bytes = audio_file.read()
                                    st.audio(audio_bytes, format='audio/wav')
                                
                                # Download button
                                st.download_button(
                                    label="💾 Download Audio",
                                    data=audio_bytes,
                                    file_name=output_filename,
                                    mime="audio/wav"
                                )
                                
                            else:
                                st.error("❌ Failed to convert document. Please try again.")
                                
                    except Exception as e:
                        st.error(f"❌ Error converting document: {str(e)}")
                        
            else:
                st.error(f"❌ Failed to extract text: {extracted_text}")
                
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")

# System Info Page
elif page == "ℹ️ System Info":
    st.markdown('<h2 class="sub-header">System Information</h2>', unsafe_allow_html=True)
    
    if pipeline:
        # Get model info
        model_info = pipeline.get_model_info()
        
        # Display system status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 System Status")
            st.success("✅ TTS Pipeline: Active")
            st.success("✅ Text Processor: Ready")
            st.success("✅ Document Processor: Ready")
            st.info(f"🔢 Loaded Models: {len(model_info['loaded_models'])}")
        
        with col2:
            st.markdown("### 📋 Supported Features")
            st.write("🎯 Text to Speech")
            st.write("📄 Document Processing")
            st.write("🔤 Text Preprocessing")
            st.write("📝 Multiple File Formats")
        
        # Model details
        st.markdown("### 🤖 Model Information")
        for lang, details in model_info['model_details'].items():
            st.write(f"**{lang.title()}:** {details.get('model_name', 'Unknown')}")
        
        # Supported formats
        st.markdown("### 📁 Supported File Formats")
        formats = pipeline.doc_processor.supported_formats
        for fmt in formats:
            st.write(f"• {fmt.upper()}")
            
        # Performance tips
        st.markdown("### ⚡ Performance Tips")
        st.info("""
        • Shorter texts (under 500 characters) process faster
        • PDF text extraction may take longer for complex documents
        • First-time model loading takes 1-2 minutes
        • Audio files are saved in WAV format for best quality
        """)
        
    else:
        st.error("❌ System not properly initialized")

# Footer
st.markdown("---")
st.markdown("*Advanced TTS System - Phase 1 Core Pipeline*")
st.markdown("*Built with Streamlit and Coqui TTS*")