# setup.py
import os
import subprocess
import sys

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        print("📦 Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("🔧 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Optional: Custom model settings
DEFAULT_MODEL_TYPE=openai
MAX_SUMMARY_LENGTH=500
DEFAULT_QUIZ_QUESTIONS=5
""")
        print("✅ .env file created!")
        print("⚠️  Please edit .env file and add your OpenAI API key")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Setting up AI Video Summarizer...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your browser")
    print("\nFor testing, run: python test_app.py")

if __name__ == "__main__":
    main()
