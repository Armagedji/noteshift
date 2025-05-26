from PIL import Image

def upscale_image(input_path, output_path, scale=2, dpi=(300, 300)):
    with Image.open(input_path) as img:
        new_size = (img.width * scale, img.height * scale)
        upscaled = img.resize(new_size, Image.LANCZOS)  # LANCZOS — лучший для масштабирования нот
        upscaled.save(output_path, dpi=dpi)

upscale_image("test1.png", "test_upscaled.png")
