from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from rembg import new_session

app = FastAPI()
session = new_session("u2netp")


@app.get("/")
def health():
    return {"ok": True, "service": "storex-rembg-service"}


@app.post("/api/remove")
async def remove_background(file: UploadFile = File(...)):
    from rembg import remove

    source = await file.read()
    output = remove(source, session=session)
    return Response(content=output, media_type="image/png")
