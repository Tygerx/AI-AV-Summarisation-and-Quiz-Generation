# app.py 
from flask import Flask, render_template, request, jsonify 
import os 
from utils.transcriber import VideoTranscriber 
from utils.summarizer import ContentSummarizer 
from utils.quiz_generator import QuizGenerator 

app = Flask(__name__) 

# Get API key from environment variable 
OPENAI_API_KEY = os.environ.get("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") 

# Initialize components 
transcriber = VideoTranscriber(api_key=OPENAI_API_KEY) 
summarizer = ContentSummarizer(api_key=OPENAI_API_KEY, model_type="openai") 
quiz_generator = QuizGenerator(api_key=OPENAI_API_KEY, model_type="openai") 

@app.route('/') 
def index(): 
    return render_template('index.html') 

@app.route('/process', methods=['POST']) 
def process_video(): 
    video_url = request.form.get('video_url') 
    # Process the video 
    try: 
        transcript, title = transcriber.process_youtube_video(video_url) 
        summary = summarizer.summarize(transcript) 
        quiz = quiz_generator.generate_quiz(transcript) 
        return render_template( 
            'results.html', 
            title=title, 
            summary=summary, 
            quiz=quiz, 
            transcript=transcript 
        ) 
    except Exception as e: 
        return jsonify({"error": str(e)}), 500 

if __name__ == '__main__': 
    app.run(debug=True)