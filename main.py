from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

# Updated imports
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

#git amk
# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI model via LangChain
llm = OpenAI(temperature=0.7)
conversation = ConversationChain(llm=llm)

# Define request and response models
class Query(BaseModel):
    text: str

class Response(BaseModel):
    reply: str

@app.post("/chat", response_model=Response)
async def chat(query: Query):
    try:
        # Use LangChain's conversation chain to get a response
        reply = conversation.predict(input=query.text)
        return Response(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
