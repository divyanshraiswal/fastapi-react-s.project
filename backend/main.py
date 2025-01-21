import uvicorn 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Fruit(BaseModel):
    name:str
    price:int

class Fruits(BaseModel):
    fruits:List[Fruit]

app=FastAPI()   

origins=[
    "http://localhost:5173",
    "http://localhost:8000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db={"fruits":[]}

@app.get("/fruits",response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory_db["fruits"])

@app.post("/fruits")
def add_fruit(fruit:Fruit):
    memory_db["fruits"].append(fruit)
    return {"message":"Fruit added successfully"}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)