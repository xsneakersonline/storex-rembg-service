from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response

app = FastAPI()
session = None


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
    output = remove(source, session=session)
    return Response(content=output, media_type="image/png")
