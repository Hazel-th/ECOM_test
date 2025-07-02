import os
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")
DEEPAI_API_URL = "https://api.deepai.org/api/nsfw-detector"


@app.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, content_type: {file.content_type}")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_bytes = await file.read()

    try:
        response = requests.post(
            DEEPAI_API_URL,
            files={"image": (file.filename, file_bytes)},
            headers={"api-key": DEEPAI_API_KEY},
        )
        response.raise_for_status()
        result = response.json()
        print("DeepAI response:", result)
        nsfw_score = result.get("output", {}).get("nsfw_score", 0)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calling DeepAI API: {str(e)}"
        )

    if nsfw_score > 0.7:
        return JSONResponse(
            content={"status": "REJECTED", "reason": "NSFW content"}, status_code=200
        )
    return JSONResponse(content={"status": "OK"}, status_code=200)
