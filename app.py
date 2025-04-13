import streamlit as st
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import io
import os
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
        /* Style the upload bar's dropzone (not the label) */
        [data-testid="stFileUploaderDropZone"], [data-testid="stFileUploader"] div[role="button"] {
            background-color: #ffffff !important;  /* White background */
            border: 1px solid #d3d3d3 !important;  /* Light gray border */
            border-radius: 5px !important;  /* Slightly rounded edges */
            padding: 10px !important;  /* Space inside */
        }
        /* Style the dropdown's select box (not the label) */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;  /* White background */
            border: 1px solid #d3d3d3 !important;  /* Light gray border */
            border-radius: 5px !important;  /* Slightly rounded edges */
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

# Add a place to upload a photo
uploaded_file = st.file_uploader("Upload your photo (JPG or PNG)", type=["jpg", "png"])

# Add a dropdown to pick a style
style = st.selectbox("Choose a style", ["Cartoon Portrait", "Vintage Photo", "Professional Headshot"])

# Check if a photo was uploaded
if uploaded_file is not None:
    # Save the uploaded file temporarily to check its size
    with open("temp_upload.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Check the file size (in MB)
    file_size = os.path.getsize("temp_upload.jpg") / (1024 * 1024)  # Convert to MB
    if file_size > 5:
        st.error("File is too large! Please upload a photo smaller than 5MB.")
        os.remove("temp_upload.jpg")  # Clean up the temporary file
    else:
        # Open and resize the photo
        image = Image.open("temp_upload.jpg")
        image = image.resize((512, 512))
        # Show the resized photo on the website
        st.image(image, caption="Resized Photo (512x512)")
        # Save the resized photo
        image.save("temp_uploaded.jpg")
        st.write("Photo resized and saved as temp_uploaded.jpg!")
        os.remove("temp_upload.jpg")  # Clean up the temporary file

        # Add a button to transform the photo
        if st.button("Transform Photo"):
            # Load the image-changing tool with safety checker disabled
            st.write("Loading the style tool... this might take a moment!")
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", safety_checker=None)
            
            # Map the style to a prompt
            style_prompts = {
                "Cartoon Portrait": "cartoon portrait",
                "Vintage Photo": "vintage photo with sepia tone",
                "Professional Headshot": "professional headshot with studio lighting"
            }
            prompt = style_prompts[style]

            # Transform the photo
            st.write(f"Transforming into {style}... please wait!")
            new_image = pipe(prompt, image=image, strength=0.3, num_inference_steps=5).images[0]
            
            # Show the transformed photo
            st.image(new_image, caption=f"Transformed Photo ({style})")
            # Save the transformed photo with a unique name using a timestamp
            timestamp = int(time.time())
            output_name = f"{style.lower().replace(' ', '_')}_{timestamp}_output.jpg"
            new_image.save(output_name)
            st.write(f"Transformed photo saved as {output_name}!")

            # Add a download button for the transformed image
            buffer = io.BytesIO()
            new_image.save(buffer, format="JPEG")
            st.download_button(
                label="Download Transformed Photo",
                data=buffer.getvalue(),
                file_name=output_name,
                mime="image/jpeg"
            )

            # Clean up the temporary resized photo
            if os.path.exists("temp_uploaded.jpg"):
                os.remove("temp_uploaded.jpg")
                st.write("Temporary file temp_uploaded.jpg deleted for privacy.")