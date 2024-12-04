import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

# Project Paths
TEMP_CODE_DIR = "./temp_manim_code"
OUTPUT_DIR = "./generated_videos"

# Verification Thresholds
VISUAL_SIMILARITY_THRESHOLD = 0.85

# Create necessary directories
os.makedirs(TEMP_CODE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
