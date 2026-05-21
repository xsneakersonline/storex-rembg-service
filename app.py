from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image, ImageOps

app = FastAPI()
session = None
MAX_INPUT_SIDE = 512


@app.get("/")
def health():
    return {"ok": True, "service": "storex-rembg-service"}


@app.post("/api/remove")
async def remove_background(file: UploadFile = File(...)):
    global session
    from rembg import new_session, remove

    if session is None:
        session = new_session("u2netp")

    source = await file.read()
    image = Image.open(BytesIO(source))
    image = ImageOps.exif_transpose(image).convert("RGB")
    image.thumbnail((MAX_INPUT_SIDE, MAX_INPUT_SIDE), Image.Resampling.LANCZOS)

    normalized = BytesIO()
    image.save(normalized, format="PNG", optimize=True)

    output = remove(normalized.getvalue(), session=session)
    return Response(content=output, media_type="image/png")
