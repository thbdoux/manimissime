from agents.developer_agent import DeveloperAgent
from agents.visual_verifier_agent import MultimodalVisualVerifier


def generate_manim_video(prompt: str, verify: bool = False):
    """
    Flexible workflow with optional verification

    Args:
        prompt (str): Animation description
        verify (bool): Whether to perform visual verification

    Returns:
        dict: Comprehensive generation results
    """
    developer = DeveloperAgent()

    # First generation attempt
    generation_result = developer.generate_and_execute(prompt)

    # If generation fails, return early
    if not generation_result["success"]:
        return generation_result

    # Optional verification
    if verify:
        verifier = MultimodalVisualVerifier()
        verification_result = verifier.verify_animation(
            prompt, generation_result["video_path"]
        )

        # Combine results if verification fails
        if not verification_result["verified"]:
            correction_prompt = (
                f"{prompt}\n\n"
                f"Verification Feedback:\n"
                f"{verification_result['details']}"
            )
            generation_result = developer.generate_and_execute(correction_prompt)

        # Merge verification results
        generation_result.update(verification_result)

    return generation_result
