from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

# Load the image-changing tool
try:
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
except Exception as e:
    print(f"Error loading the tool: {e}")
    exit()

# Open and resize the photo
try:
    image = Image.open("sample.jpg")
    image = image.resize((512, 512))
except Exception as e:
    print(f"Error opening or resizing sample.jpg: {e}")
    exit()

# List of styles to try
styles = ["cartoon portrait", "vintage photo with sepia tone", "professional headshot with studio lighting"]

# Transform the photo into each style
for style in styles:
    try:
        print(f"Trying to transform into '{style}'...")
        new_image = pipe(style, image=image, strength=0.75).images[0]
        # Save with a name based on the style (e.g., cartoon_output.jpg, vintage_output.jpg)
        output_name = style.split()[0] + "_output.jpg"
        new_image.save(output_name)
        print(f"Transformed photo into '{style}' and saved as {output_name}!")
    except Exception as e:
        print(f"Error transforming into '{style}': {e}")