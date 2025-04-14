import streamlit as st
from diffusers import StableDiffusionPipeline
import io
import time

# Add some basic CSS styling
st.markdown("""
    <style>
        /* Background for the entire app */
        .stApp {
            background-color: #f5f5f5 !important;  /* Very light gray background */
        }
        /* Style the title */
        [data-testid="stMarkdownContainer"] h1 {
            color: #333333 !important;  /* Dark gray title */
            text-align: center !important;
            margin-top: 20px !important;  /* Add space above the title */
        }
        /* Style the buttons */
        .stButton>button {
            background-color: #007bff !important;  /* Blue button */
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 5px !important;
            border: none !important;
        }
        .stButton>button:hover {
            background-color: #0056b3 !important;  /* Darker blue on hover */
        }
        /* Style the navigation menu (like "Deploy") */
        header, [data-testid="stHeader"], [data-testid="stToolbar"] {
            background-color: #f5f5f5 !important;  /* Match the very light gray background */
            box-shadow: none !important;  /* Remove any default shadow */
        }
        /* Target the toolbar's parent container */
        div:has([data-testid="stToolbar"]) {
            background-color: #f5f5f5 !important;
        }
        /* Style the buttons and text in the toolbar */
        [data-testid="stToolbar"] button, [data-testid="stToolbar"] button > div, [data-testid="stToolbar"] button > div > p {
            color: #333333 !important;  /* Dark gray text for "Deploy" */
            background-color: transparent !important;  /* No background on buttons */
        }
        /* Ensure text labels are visible */
        label, p {
            color: #333333 !important;  /* Dark gray text for labels */
            background-color: transparent !important;  /* No background for labels */
        }
    </style>
""", unsafe_allow_html=True)

# Show a title on the website
st.title("Photo Generator")

# Add a text input for the photo description
photo_prompt = st.text_input("Describe the photo you want to generate (e.g., 'a sunny beach with palm trees')", value="a sunny beach with palm trees")

# Add a button to generate the photo
if st.button("Generate Photo"):
    # Validate the prompt
    if not photo_prompt.strip():
        st.error("Please enter a description for the photo.")
    else:
        # Load the text-to-image model
        st.write("Loading the generation tool... this might take a moment!")
        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", safety_checker=None)
        
        # Generate the photo
        st.write(f"Generating photo: {photo_prompt}... please wait!")
        new_image = pipe(photo_prompt, num_inference_steps=5).images[0]
        
        # Show the generated photo
        st.image(new_image, caption=f"Generated Photo: {photo_prompt}")
        # Save the generated photo with a unique name using a timestamp
        timestamp = int(time.time())
        output_name = f"generated_photo_{timestamp}.jpg"
        new_image.save(output_name)
        st.write(f"Generated photo saved as {output_name}!")

        # Add a download button for the generated image
        buffer = io.BytesIO()
        new_image.save(buffer, format="JPEG")
        st.download_button(
            label="Download Generated Photo",
            data=buffer.getvalue(),
            file_name=output_name,
            mime="image/jpeg"
        )