import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY não foi encontrada no arquivo .env")

client = OpenAI(api_key=api_key)


class MessageRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(message: MessageRequest):
    response = client.responses.create(
        model="gpt-4",
        input=message.message,
    )

    model_reply = response.output_text
    return {"message": model_reply}
