from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def resize_image(image, width, height):
   
    img = Image.open(image)

    # Resize the image
    img = img.resize((width, height), Image.ANTIALIAS)

    # Create a BytesIO buffer to temporarily store the resized image
    buffer = BytesIO()

    # Save the resized image to the buffer in the format you want (e.g., JPEG)
    img.save(buffer, format='JPEG')

    # Create a new InMemoryUploadedFile from the buffer
    resized_image = InMemoryUploadedFile(
        buffer,
        None,
        f"{image.name}.jpg",
        'image/jpeg',
        buffer.tell(),
        None
    )

    return resized_image