from PIL import Image, ImageDraw

# Create a 256x256 image with a transparent background
icon_size = 256
image = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a simple icon (a document with a magnifying glass)
# Document
draw.rectangle([64, 32, 192, 224], fill=(53, 53, 53))
draw.rectangle([96, 32, 192, 64], fill=(42, 130, 218))

# Magnifying glass
glass_color = (42, 130, 218)
handle_color = (42, 130, 218)
draw.ellipse([128, 96, 192, 160], outline=glass_color, width=8)
draw.line([176, 144, 208, 176], fill=handle_color, width=8)

# Save the icon
image.save('app_icon.ico', format='ICO', sizes=[(256, 256)]) 