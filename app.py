import streamlit as st
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import generate_manim_video


def main():
    st.title("Manim Animation Generator")

    # Prompt input
    prompt = st.text_area(
        "Enter Animation Prompt",
        placeholder="Describe your desired Manim animation...",
        height=150,
    )

    # Verification toggle
    verify = st.checkbox("Enable Visual Verification", value=False)

    # Generate button
    if st.button("Generate Animation"):
        if prompt:
            # Show loading spinner
            with st.spinner("Generating Animation..."):
                # Run generation with optional verification
                result = generate_manim_video(prompt, verify=verify)

            # Display results
            if result.get("success", False):
                st.success("Animation Generated Successfully!")

                # Display verification status if verification was enabled
                if verify:
                    verified = result.get("verified", False)
                    st.metric("Verification", "Passed" if verified else "Failed")

                    # Show verification details if not verified
                    if not verified:
                        st.warning(result.get("details", "No details available"))

                # Display video if generated
                video_path = result.get("video_path")
                if video_path and os.path.exists(video_path):
                    st.video(video_path)
                else:
                    st.error("Video file not found")
            else:
                st.error("Failed to generate animation")
        else:
            st.warning("Please enter a prompt")


if __name__ == "__main__":
    main()
