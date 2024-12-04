import os
import subprocess
import tempfile
from typing import Tuple, Optional


class CodeExecutor:
    @staticmethod
    def execute_manim_code(code: str, output_dir: str) -> Tuple[bool, Optional[str]]:
        """
        Execute Manim code and return execution status and video path

        Args:
            code (str): Manim Python code to execute
            output_dir (str): Directory to save output

        Returns:
            Tuple[bool, Optional[str]]: Execution status and output video path
        """
        # try:
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Extract filename without extension
        filename = os.path.splitext(os.path.basename(temp_file_path))[0]

        # Execute Manim command
        result = subprocess.run(
            ["manim", "-qh", temp_file_path],  # High quality
            capture_output=True,
            text=True,
        )

        # Check for successful execution
        if result.returncode == 0:
            # Construct the full path to the video directory
            media_dir = os.path.join("media", "videos", filename, "1080p60")

            # Find all MP4 files in the directory
            video_files = [
                os.path.join(media_dir, f)
                for f in os.listdir(media_dir)
                if f.endswith(".mp4")
            ]

            # Find the latest video file
            if video_files:
                latest_video = max(video_files, key=os.path.getctime)
                return True, latest_video
            else:
                print("No video files found in the directory")
                return False, None
        else:
            print(f"Execution Error: {result.stderr}")
            return False, None

        # except Exception as e:
        #     print(f"Execution Exception: {e}")
        #     return False, None
        # finally:
        #     # Clean up temporary file
        #     if 'temp_file_path' in locals():
        #         os.unlink(temp_file_path)
