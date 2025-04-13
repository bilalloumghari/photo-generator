# Photo Generator

This is a Streamlit app that transforms photos into different styles using Stable Diffusion. You can upload a photo, choose a style (Cartoon Portrait, Vintage Photo, or Professional Headshot), and download the transformed image.

## Features
- Upload a photo (JPG or PNG, under 5MB).
- Choose from three styles: Cartoon Portrait, Vintage Photo, or Professional Headshot.
- Transform the photo using Stable Diffusion.
- Download the styled photo.
- Temporary files are deleted after processing for privacy.

## How to Use
1. Visit the app at: https://photo-generator-uohixjwv75cji5qrpshca4.streamlit.app/
2. Upload a photo (JPG or PNG, under 5MB).
3. Select a style from the dropdown menu.
4. Click "Transform Photo" and wait for the transformation (about 1 minute).
5. Download the styled photo using the "Download Transformed Photo" button.

## Limitations
- Transformation takes about 1 minute due to CPU limitations (target was <15 seconds, which requires a GPU for better performance).
- The app can only handle one transformation at a time; multiple simultaneous transformations may cause crashes.
- Styles may not always perfectly match the input photo due to low `num_inference_steps` (set to 5 for speed).

## Setup for Local Development
1. Clone the repository: `git clone https://github.com/bilalloumghari/photo-generator.git`
2. Navigate to the project folder: `cd photo-generator`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `venv\Scripts\activate` (on Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run the app: `streamlit run app.py`

## Dependencies
- Streamlit
- Diffusers
- Torch
- Transformers
- Pillow
- Accelerate
- See `requirements.txt` for full list.

## Future Improvements
- Add a task queue to handle multiple simultaneous transformations.
- Optimize transformation speed further (e.g., use a GPU or a lighter model).
- Improve style quality by increasing `num_inference_steps` or `strength`.

## License
MIT License