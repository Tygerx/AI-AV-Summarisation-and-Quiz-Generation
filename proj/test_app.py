# test_app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.transcriber import VideoTranscriber
from utils.summarizer import ContentSummarizer
from utils.quiz_generator import QuizGenerator

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        print("✅ Testing imports...")
        
        # Test transcriber
        transcriber = VideoTranscriber("test_key")
        print("✅ VideoTranscriber imported successfully")
        
        # Test summarizer
        summarizer = ContentSummarizer("test_key")
        print("✅ ContentSummarizer imported successfully")
        
        # Test quiz generator
        quiz_generator = QuizGenerator("test_key")
        print("✅ QuizGenerator imported successfully")
        
        print("\n🎉 All imports successful! The application is ready to run.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Run: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_imports()
