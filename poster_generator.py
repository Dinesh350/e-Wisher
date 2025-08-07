import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
def load_image(photo_url):
    if photo_url.startswith("http://") or photo_url.startswith("https://"):
        # Load from URL
        response = requests.get(photo_url)
        return Image.open(BytesIO(response.content))
    else:
        # Load from local path
        return Image.open(photo_url)
# Call your Node.js server to fetch birthday data
res = requests.get("http://localhost:8008/birthdays-today")
if res.status_code != 200:
    print("No birthdays or error occurred.")
    exit()

birthdays = res.json()

# Path to the birthday template image (update this if you move the file)
template_path = r"C:\Users\class\OneDrive\Desktop\IDP\img0.webp"

# Output folder for posters
output_dir = os.path.join("C:\\Users\\class\\OneDrive\\Desktop\\IDP", "posters")
os.makedirs(output_dir, exist_ok=True)

for person in birthdays:
    name = person['reg_no']
    photo_url = person.get('photo_url')

    if not photo_url:
        print(f"No photo URL for {name}, skipping.")
        continue

    # Load photo (either local or download from URL)
    try:
        if os.path.exists(photo_url):  # Local path
            print(f"Using local image for {name}.")
            photo = Image.open(photo_url).convert("RGBA")
        else:  # Remote URL
            photo_res = requests.get(photo_url)
            if photo_res.status_code != 200:
                print(f"Failed to download photo for {name}, skipping.")
                continue
            photo = Image.open(BytesIO(photo_res.content)).convert("RGBA")
    except Exception as e:
        print(f"Error loading photo for {name}: {e}")
        continue

    # Open template
    try:
        template = Image.open(template_path).convert("RGBA")
    except FileNotFoundError:
        print("Template file not found. Please check the path.")
        exit()

        # Resize and paste the photo
    photo = photo.resize((180, 160))  # Adjusted size
    photo_position = (195, 180)       # Adjusted position
    template.paste(photo, photo_position, mask=photo)


    # Draw the name text
    draw = ImageDraw.Draw(template)
    try:
        font = ImageFont.truetype("segoesc.ttf", 26)
    except IOError:
        font = ImageFont.load_default()

    text_position = (290, 375)
    draw.text(text_position, name, font=font, fill=(0, 0, 0), anchor="ms")

    # Save the poster
    output_path = os.path.join(output_dir, f"{name.replace(' ', '_')}_poster.jpg")
    template.convert("RGB").save(output_path)
    print(f"Poster saved: {output_path}")
    print("Local file exists:", os.path.exists(photo_url))

