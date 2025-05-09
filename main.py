from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # This will read the .env file and load the variables into the environment

# Get the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Allow CORS from the frontend (React app on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow the frontend React app to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize the OpenAI client, passing the API key from the environment
client = OpenAI(api_key=api_key)

# Define the request data model using Pydantic
class StoryRequest(BaseModel):
    character: str
    theme: str
    setting: str

# Define the response model to return the generated story
class StoryResponse(BaseModel):
    story: str

# Create the endpoint to generate the story
@app.post("/generate-story/", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    # Create the input string (prompt) based on user input
    prompt = f"Write a fairy tale where {request.character} goes on an adventure in a {request.setting} with a theme of {request.theme}."

    try:
        # Call the OpenAI API to generate a story using the client
        response = client.responses.create(
            model="gpt-4.1",  # Use the appropriate model (e.g., GPT-4.1 or GPT-4)
            input=prompt        # Provide the prompt to the model
        )

        # Extract the story from the response object
        generated_story = response.output_text.strip()

        # Return the generated story as a response
        return StoryResponse(story=generated_story)
    
    except Exception as e:
        # If any error occurs, return the error message
        return {"error": str(e)}
