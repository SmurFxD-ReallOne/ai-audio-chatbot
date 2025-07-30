import os
import json
import tempfile
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import speech_recognition as sr
import cohere
from gtts import gTTS
import io
import wave
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Cohere client
cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def audio_to_text(self, audio_data):
        """Convert audio data to text using Google Speech Recognition"""
        try:
            # Decode base64 audio data
            if ',' in audio_data:
                audio_bytes = base64.b64decode(audio_data.split(',')[1])
            else:
                audio_bytes = base64.b64decode(audio_data)
            
            # Try multiple approaches for audio processing
            text = self.try_audio_processing_methods(audio_bytes)
            
            if text and not text.startswith("Error") and not text.startswith("Audio processing failed"):
                return text
            else:
                return "I couldn't understand the audio. Please try speaking more clearly and make sure your microphone is working properly."
                
        except Exception as e:
            return "I couldn't process the audio. Please try again or use text input instead."
    
    def try_audio_processing_methods(self, audio_bytes):
        """Try different methods to process audio"""
        methods = [
            self.method_1_direct_webm,
            self.method_2_simple_wav,
            self.method_3_audio_segment
        ]
        
        for method in methods:
            try:
                result = method(audio_bytes)
                if result and not result.startswith("Error"):
                    return result
            except Exception as e:
                print(f"Method failed: {e}")
                continue
        
        return "Audio processing failed: Could not convert audio to text"
    
    def method_1_direct_webm(self, audio_bytes):
        """Method 1: Try direct WebM processing"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name
            
            with sr.AudioFile(temp_audio_path) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
            
            os.unlink(temp_audio_path)
            return text if text else None
            
        except Exception as e:
            if 'temp_audio_path' in locals():
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass
            raise e
    
    def method_2_simple_wav(self, audio_bytes):
        """Method 2: Create simple WAV file"""
        try:
            # Create a basic WAV header
            wav_data = self.create_wav_header(audio_bytes)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav:
                temp_wav.write(wav_data)
                wav_path = temp_wav.name
            
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
            
            os.unlink(wav_path)
            return text if text else None
            
        except Exception as e:
            if 'wav_path' in locals():
                try:
                    os.unlink(wav_path)
                except:
                    pass
            raise e
    
    def method_3_audio_segment(self, audio_bytes):
        """Method 3: Try with audio segment approach"""
        try:
            # Try to process as raw audio data
            with tempfile.NamedTemporaryFile(delete=False, suffix='.raw') as temp_raw:
                temp_raw.write(audio_bytes)
                raw_path = temp_raw.name
            
            # Try to read as raw audio
            with sr.AudioFile(raw_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
            
            os.unlink(raw_path)
            return text if text else None
            
        except Exception as e:
            if 'raw_path' in locals():
                try:
                    os.unlink(raw_path)
                except:
                    pass
            raise e
    
    def create_wav_header(self, audio_bytes):
        """Create a basic WAV header"""
        header = bytearray(44)
        
        # RIFF header
        header[0:4] = b'RIFF'
        header[4:8] = (len(audio_bytes) + 36).to_bytes(4, 'little')
        header[8:12] = b'WAVE'
        
        # fmt chunk
        header[12:16] = b'fmt '
        header[16:20] = (16).to_bytes(4, 'little')
        header[20:22] = (1).to_bytes(2, 'little')  # PCM
        header[22:24] = (1).to_bytes(2, 'little')  # mono
        header[24:28] = (16000).to_bytes(4, 'little')  # sample rate
        header[28:32] = (32000).to_bytes(4, 'little')  # byte rate
        header[32:34] = (2).to_bytes(2, 'little')  # block align
        header[34:36] = (16).to_bytes(2, 'little')  # bits per sample
        
        # data chunk
        header[36:40] = b'data'
        header[40:44] = len(audio_bytes).to_bytes(4, 'little')
        
        return header + audio_bytes
    
    def text_to_audio(self, text, language='en'):
        """Convert text to audio using Google Text-to-Speech"""
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                tts.save(temp_audio.name)
                temp_audio_path = temp_audio.name
            
            # Read the audio file and convert to base64
            with open(temp_audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Clean up temporary file
            os.unlink(temp_audio_path)
            
            return f"data:audio/mp3;base64,{audio_base64}"
        except Exception as e:
            return f"Error converting text to audio: {str(e)}"

class LLMProcessor:
    def __init__(self, client):
        self.client = client
    
    def generate_response(self, user_input, conversation_history=None):
        """Generate response using Cohere LLM"""
        try:
            # Don't process error messages as user input
            if user_input.startswith("Error") or user_input.startswith("Audio processing failed") or user_input.startswith("I couldn't"):
                return "I'm having trouble understanding your audio. Please try speaking more clearly or use the text input instead."
            
            # Prepare the conversation context
            if conversation_history is None:
                conversation_history = []
            
            # Create the prompt with conversation history
            prompt = "You are a helpful AI assistant. Please provide a clear and concise response to the user's question or statement.\n\n"
            
            # Add conversation history
            for msg in conversation_history[-5:]:  # Keep last 5 messages for context
                prompt += f"{msg['role']}: {msg['content']}\n"
            
            prompt += f"User: {user_input}\nAssistant:"
            
            # Generate response using Cohere
            response = self.client.generate(
                model='command',
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            
            return response.generations[0].text.strip()
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

# Initialize processors
audio_processor = AudioProcessor()
llm_processor = LLMProcessor(cohere_client)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Process audio input and return text response"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        audio_data = data.get('audio')
        
        if not audio_data:
            return jsonify({'error': 'No audio data provided'}), 400
        
        # Convert audio to text
        text = audio_processor.audio_to_text(audio_data)
        
        # Check if audio processing failed
        if text.startswith("I couldn't") or text.startswith("Audio processing failed"):
            return jsonify({'error': text}), 400
        
        # Generate LLM response
        response_text = llm_processor.generate_response(text)
        
        # Convert response to audio
        response_audio = audio_processor.text_to_audio(response_text)
        
        return jsonify({
            'user_text': text,
            'response_text': response_text,
            'response_audio': response_audio
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/process_text', methods=['POST'])
def process_text():
    """Process text input and return audio response"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_text = data.get('text')
        
        if not user_text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate LLM response
        response_text = llm_processor.generate_response(user_text)
        
        # Convert response to audio
        response_audio = audio_processor.text_to_audio(response_text)
        
        return jsonify({
            'user_text': user_text,
            'response_text': response_text,
            'response_audio': response_audio
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 