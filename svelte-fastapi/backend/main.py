from typing import  Dict
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Allow your Svelte app origin
origins = [
    "http://localhost:3000",  # Replace with your local dev URL or production URL
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", response_model=Dict[str, str])
async def root():
    return {"title": "Hello you successfully connected to the backend!", "subtitle": "You learn how to set up a docker compose file and use FastAPi with Svelte app."}


@app.get("/first", response_model=Dict[str, str])
async def get_first_page():
  return {"title": "First page", "subtitle": "This is the first page!"}

@app.get("/second", response_model=Dict[str, str])
async def get_second_page():

  return {"title": "Second page", "subtitle": "This is the second page!"}