import hmac, hashlib
import json
import uvicorn
import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi import Request, Header, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_signature(raw_body: bytes, signature_hex: str) -> bool:
    if not signature_hex or not WEBHOOK_SECRET:
        return False
    digest = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(digest, signature_hex)


@app.post("/checkout/webhook", response_class=PlainTextResponse)
async def checkout_webhook(request: Request, x_signature: str = Header(default="")):
    raw_body = await request.body()

    if not verify_signature(raw_body, x_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    try:
        payload = json.loads(raw_body.decode("utf-8"))
        print("Nhận được webhook:", payload)
        
        # TODO: Xử lý logic nghiệp vụ của bạn tại đây
        # Ví dụ: Cập nhật trạng thái đơn hàng, gửi email xác nhận, v.v.
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    return "ok"


if __name__ == "__main__":
    uvicorn.run(
        "mainr:app", host="0.0.0.0", port=8000, reload=True, log_level="debug"
    )
