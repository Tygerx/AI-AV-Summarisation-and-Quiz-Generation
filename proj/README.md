# AI Video Summarizer & Quiz Generator

A powerful web application that processes YouTube videos to generate automatic transcriptions, intelligent summaries, and interactive quizzes using OpenAI's Whisper and GPT-4 models.

## Features

- 🎥 **YouTube Video Processing**: Download and process any YouTube video
- 🎤 **Automatic Transcription**: Convert audio to text using OpenAI Whisper
- 📝 **Smart Summarization**: Generate concise summaries using GPT-4
- ❓ **Interactive Quizzes**: Create multiple-choice questions from video content
- 🎨 **Modern UI**: Beautiful, responsive web interface
- 📱 **Mobile Friendly**: Works on all devices

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Enter YouTube URL**: Paste any YouTube video URL in the input field
2. **Process Video**: Click "Process Video" to start the analysis
3. **View Results**: Get the transcription, summary, and interactive quiz
4. **Take Quiz**: Answer questions and check your knowledge
5. **Copy Content**: Use copy buttons to save results

## API Requirements

- **OpenAI API Key**: Required for Whisper transcription and GPT-4 summarization/quiz generation
- **Internet Connection**: Required for YouTube video downloading

## File Structure

```
proj/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main upload page
│   └── results.html      # Results display page
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── main.js       # Frontend JavaScript
└── utils/
    ├── transcriber.py    # Video transcription logic
    ├── summarizer.py     # Content summarization
    └── quiz_generator.py # Quiz generation
```

## Troubleshooting

### Common Issues

1. **YouTube Download Errors**: Some videos may be restricted or unavailable
2. **API Rate Limits**: OpenAI has usage limits - check your account
3. **Large Videos**: Very long videos may take longer to process
4. **Audio Quality**: Poor audio quality may affect transcription accuracy

### Error Messages

- "No suitable video stream found": Video format not supported
- "Transcription Error": Check OpenAI API key and internet connection
- "Summary Error": GPT-4 API issue or content too long

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
