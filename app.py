from io import BytesIO
from statistics import median

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image, ImageFilter, ImageOps

app = FastAPI()
MAX_INPUT_SIDE = 1024


@app.get("/")
def health():
    return {"ok": True, "service": "storex-rembg-service"}


def _median_corner_background(image):
    width, height = image.size
    patch = max(8, min(48, min(width, height) // 12))
    pixels = image.load()
    samples = []

    corners = (
        (0, 0),
        (max(0, width - patch), 0),
        (0, max(0, height - patch)),
        (max(0, width - patch), max(0, height - patch)),
    )

    for left, top in corners:
        for y in range(top, min(height, top + patch)):
            for x in range(left, min(width, left + patch)):
                samples.append(pixels[x, y])

    if not samples:
        return (255, 255, 255)

    return tuple(int(median(channel)) for channel in zip(*samples))


def _build_alpha(image, background):
    width, height = image.size
    source = image.load()
    alpha = Image.new("L", image.size, 0)
    alpha_pixels = alpha.load()

    for y in range(height):
        for x in range(width):
            r, g, b = source[x, y]
            distance = ((r - background[0]) ** 2 + (g - background[1]) ** 2 + (b - background[2]) ** 2) ** 0.5
            value = int(max(0, min(255, (distance - 18) * 5.2)))
            alpha_pixels[x, y] = value

    return alpha.filter(ImageFilter.GaussianBlur(1.2))


@app.post("/api/remove")
async def remove_background(file: UploadFile = File(...)):
    source = await file.read()
    image = Image.open(BytesIO(source))
    image = ImageOps.exif_transpose(image).convert("RGB")
    image.thumbnail((MAX_INPUT_SIDE, MAX_INPUT_SIDE), Image.Resampling.LANCZOS)

    background = _median_corner_background(image)
    alpha = _build_alpha(image, background)
    output = image.convert("RGBA")
    output.putalpha(alpha)

    buffer = BytesIO()
    output.save(buffer, format="PNG", optimize=True)
    return Response(content=buffer.getvalue(), media_type="image/png")
