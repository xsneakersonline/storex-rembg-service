from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response

app = FastAPI()


@app.get("/")
def health():
    return {"ok": True, "service": "storex-rembg-service"}


@app.post("/api/remove")
async def remove_background(file: UploadFile = File(...)):
    # Import lazily so Render can bind the HTTP port before rembg/model startup work.
    from rembg import remove

    source = await file.read()
    output = remove(source)
    return Response(content=output, media_type="image/png")
