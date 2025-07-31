# Audio Chatbot

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Cohere](https://img.shields.io/badge/Cohere-AI-orange.svg)](https://cohere.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

A complete **audio-to-text-to-audio chatbot** system that allows users to interact with an intelligent assistant using voice or text input, with responses provided in both text and audio formats.

## Demo

![Audio Chatbot Demo](demo.gif)

*Demo showing voice interaction with the assistant*

## Features

- **Voice Input**: Record audio and convert to text using browser speech recognition
- **Intelligent Responses**: Generate smart responses using Cohere's LLM
- **Audio Output**: Convert responses to speech using Google Text-to-Speech
- **Text Input**: Alternative text-based interaction
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Processing**: Live speech recognition and processing
- **Beautiful UI**: Gradient design with smooth animations
- **Browser Compatible**: Works on Chrome, Edge, Safari, and Firefox

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Microphone access (for voice input)
- Cohere API key (free tier available)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-audio-chatbot.git
   cd ai-audio-chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   - Get a free API key from [Cohere Dashboard](https://dashboard.cohere.com/)
   - Create a `.env` file in the project root:
   ```bash
   COHERE_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

6. **To stop the server**: Press `Ctrl+C` in the terminal

**Note**: The chatbot only works while the server is running. When you stop the server, the web interface will not be able to connect to the backend.

## How to Use

### Voice Interaction
1. Click the **"Start Recording"** button
2. Speak your message clearly
3. The browser will automatically convert your speech to text
4. Receive response in both text and audio formats

### Text Interaction
1. Type your message in the text area
2. Click **"Send Text"** or press Enter
3. Receive response in both text and audio formats

## Technical Architecture

### Backend (Flask)
- **Web Framework**: Flask with CORS support
- **Speech Recognition**: Browser-based Web Speech API
- **LLM Integration**: Cohere's Command model for intelligent responses
- **Text-to-Speech**: Google TTS for audio output
- **REST API**: Clean endpoints for processing

### Frontend (HTML/CSS/JavaScript)
- **Modern UI**: Responsive design with gradient backgrounds
- **Speech Recognition**: Browser-based Web Speech API
- **Real-time Updates**: Dynamic conversation display
- **Error Handling**: User-friendly error messages
- **Audio Playback**: Built-in audio player

### Key Components

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── setup_api_key.py     # API key setup script
└── README.md           # This file
```

## API Endpoints

- `GET /` - Serve the main web interface
- `POST /process_audio` - Process audio input and return response
- `POST /process_text` - Process text input and return response

## Customization

### Changing the Model
Edit the `LLMProcessor` class in `app.py`:
```python
response = self.client.generate(
    model='command',  # Change to other Cohere models
    prompt=prompt,
    max_tokens=150,   # Adjust response length
    temperature=0.7,  # Adjust creativity (0.0-1.0)
)
```

### Modifying the UI
- Edit `templates/index.html` for layout changes
- Modify CSS styles in the `<style>` section
- Update JavaScript in the `<script>` section

### Adding New Features
- Extend the `AudioProcessor` class for different TTS engines
- Add conversation history persistence
- Implement user authentication
- Add support for multiple languages

## Troubleshooting

### Common Issues

1. **Microphone not working**:
   - Ensure browser has microphone permissions
   - Check if microphone is not being used by other applications
   - Try refreshing the page

2. **API Key errors**:
   - Verify your Cohere API key is correct
   - Check if the `.env` file is in the project root
   - Ensure the API key has sufficient credits

3. **Speech recognition not working**:
   - Use Chrome, Edge, or Safari for best compatibility
   - Ensure you're on HTTPS or localhost
   - Check browser console for errors

4. **Audio playback issues**:
   - Ensure browser supports audio playback
   - Check if audio files are being generated correctly

### Browser Compatibility

- **Chrome**: Full support for speech recognition
- **Edge**: Full support for speech recognition
- **Safari**: Full support for speech recognition
- **Firefox**: Limited support (will fall back to audio recording)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project!

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the browser console
3. Check the Flask server logs for backend errors
4. Open an issue on GitHub

## Project Status

**COMPLETE AND WORKING**

This project successfully implements:
- Audio input to text conversion
- LLM-powered responses using Cohere
- Text-to-speech audio output
- Modern web interface
- Cross-browser compatibility

## Author

**Musaad Al-Ghashmari**

---

**Enjoy chatting with your assistant!** 