from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import base64
import config


class VerificationResult(BaseModel):
    verified: bool = Field(
        description="Whether the animation fully meets the original prompt requirements"
    )
    details: str = Field(
        description="Explanation of verification result, including specific issues if not verified"
    )


class MultimodalVisualVerifier:
    def __init__(self):
        # System prompt for verification
        self.system = """You are an expert visual verification assistant.
        Carefully analyze the image and determine if it matches the given animation prompt.
        Provide a structured, objective assessment."""

        # Output parser
        self.parser = PydanticOutputParser(pydantic_object=VerificationResult)

        # Multimodal LLM (assuming OpenAI's GPT-4o or similar)
        self.llm = ChatOpenAI(
            model="gpt-4o", temperature=0.3  # Update with actual multimodal model
        )

        # Prompt template for multimodal verification
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system),
                ("human", "Prompt: {prompt}"),
                (
                    "human",
                    [
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64,{input_img}"},
                        }
                    ],
                ),
                ("human", "{format_instructions}"),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

        # Create chain
        self.chain = self.prompt | self.llm | self.parser

    def _image_to_base64(self, image_path):
        """
        Convert image to base64 encoded string

        Args:
            image_path (str): Path to the image file

        Returns:
            str: Base64 encoded image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def extract_last_frame(self, video_path):
        """
        Extract last frame from video as image

        Args:
            video_path (str): Path to the video file

        Returns:
            str: Path to extracted image
        """
        import cv2

        # Open video
        video = cv2.VideoCapture(video_path)

        # Get total number of frames
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Set to last frame
        video.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

        # Read last frame
        success, frame = video.read()
        if not success:
            raise ValueError("Could not extract last frame")

        # Save frame as image
        output_path = f"{video_path}_last_frame.jpg"
        cv2.imwrite(output_path, frame)

        return output_path

    def verify_animation(self, prompt: str, video_path: str) -> dict:
        """
        Verify animation conformity to prompt

        Args:
            prompt (str): Original animation description
            video_path (str): Path to the generated video

        Returns:
            dict: Verification results
        """
        try:
            # Extract last frame
            frame_path = self.extract_last_frame(video_path)

            # Convert to base64
            base64_image = self._image_to_base64(frame_path)

            # Run verification chain
            verification_result = self.chain.invoke(
                {"prompt": prompt, "input_img": base64_image}
            )

            return {
                "verified": verification_result.verified,
                "details": verification_result.details,
                "video_path": video_path,
            }

        except Exception as e:
            return {
                "verified": False,
                "details": f"Verification failed: {str(e)}",
                "video_path": video_path,
            }
