import re
import base64
from PIL import Image
import io

def process():
    with open("index (7).html", "r") as f:
        content = f.read()

    # Find the logo base64 (looking at nav-logo img)
    # The logo was PNG
    match = re.search(r'(data:image/[a-zA-Z]+;base64,([A-Za-z0-9+/=\s]+))', content)
    if not match:
        print("Logo not found")
        return

    full_match = match.group(1)
    b64_data = match.group(2).replace('\n', '').replace('\r', '').replace(' ', '')
    image_data = base64.b64decode(b64_data)
    
    image = Image.open(io.BytesIO(image_data)).convert("RGBA")
    
    # Process image:
    # Corner pixel is likely the background
    pixels = image.load()
    width, height = image.size
    bg_color = pixels[0, 0] # Top-left corner
    
    if bg_color[3] > 0: # If it's not already transparent
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                # If color is close to bg_color
                if abs(r - bg_color[0]) < 30 and abs(g - bg_color[1]) < 30 and abs(b - bg_color[2]) < 30:
                    pixels[x, y] = (255, 255, 255, 0)
    
    # Save back to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    new_b64_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    new_full_string = "data:image/png;base64," + new_b64_data
    
    # Replace in HTML
    new_content = content.replace(full_match, new_full_string)
    
    with open("index (7).html", "w") as f:
        f.write(new_content)
        
    print("Logo processed and HTML updated")

process()
