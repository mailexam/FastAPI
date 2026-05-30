import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from mail import send_test

load_dotenv()

app = FastAPI()


class SendRequest(BaseModel):
    to: EmailStr = "user@example.test"
    subject: str = "FastAPI + Mailexam"
    body: str = "Mailexam test from FastAPI"


@app.post("/mail/test")
async def mail_test(payload: SendRequest):
    await asyncio.to_thread(
        send_test,
        to=str(payload.to),
        subject=payload.subject,
        body=payload.body,
    )
    return {"status": "ok"}
