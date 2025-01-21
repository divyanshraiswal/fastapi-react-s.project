# fastapi-react-s.project

## Fruit Management App

## Overview
This project consists of a **Full-Stack Web Application** that allows users to manage a list of fruits. It uses **FastAPI** for the backend and **React** for the frontend.

## Backend (FastAPI)
- The backend is built using **FastAPI**, a modern and fast web framework for Python.
- It exposes two API endpoints:
  - `GET /fruits`: Fetches a list of fruits stored in memory.
  - `POST /fruits`: Adds a new fruit to the memory database.
- **CORS (Cross-Origin Resource Sharing)** is configured to allow requests from a specified origin (`http://localhost:3000`), enabling communication between the frontend (running on a different port) and the backend.
- The backend is run with **Uvicorn**, a high-performance ASGI server.

## Frontend (React)
- The frontend is built using **React**, a popular JavaScript library for building user interfaces.
- It includes the following components:
  - **FruitList**: Displays a list of fruits and interacts with the backend API to fetch and add fruits.
  - **AddFruitForm**: A form for submitting new fruits to the backend.
- **Axios** is used to make HTTP requests to the FastAPI backend to fetch and add fruits.
- The application is structured to include an `App` component that renders the fruit list and the form to add fruits.

## Project Workflow
1. The user interacts with the **React frontend**, adding a fruit name through the **AddFruitForm** component.
2. The form sends a `POST` request to the backend, which updates the list of fruits stored in memory.
3. The **FruitList** component periodically fetches the updated list of fruits from the backend using a `GET` request.
4. The list of fruits is displayed, and the user can add more fruits.

## Setup Instructions

### Backend Setup
1. Create a `backend` directory and navigate to it:
   ```bash
   mkdir backend
   cd backend


### Dependencies

- Python 3.9+

### Setup

- `mkdir backend`
- `cd backend`
- Create a virtual environment: `python3 -m venv venv`
- Activate the virtual environment:
  - Mac/Linux: `source ./venv/bin/activate`
  - Windows: `.\venv\Scripts\activate`
- Install the dependencies from [requirements.txt](./backend/requirements.txt)
  - `pip install -r requirements.txt`

### Basic FastAPI Without Auth

```python
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Fruit(BaseModel):
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]
    
app = FastAPI(debug=True)

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"fruits": []}

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory_db["fruits"])

@app.post("/fruits")
def add_fruit(fruit: Fruit):
    memory_db["fruits"].append(fruit)
    return fruit
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run the API

- `python main.py`

## React Setup

### Dependencies 

- NodeJS

### Setup 

- `npm create vite@latest frontend --template react`
- `cd frontend`
- `npm install`
- `npm install axios`

### Components

- Make the following dir structure
  - src/
    - components/
      - Fruits.jsx
      - AddFruitForm.jsx
    - App.jsx
    - main.jsx
    - api.js

### Fruits.jsx

```jsx
import React, { useEffect, useState } from 'react';
import api from "../api.js";
import AddFruitForm from './AddFruitForm';

const FruitList = () => {
  const [fruits, setFruits] = useState([]);

  const fetchFruits = async () => {
    try {
      const response = await api.get('/fruits');
      setFruits(response.data.fruits);
    } catch (error) {
      console.error("Error fetching fruits", error);
    }
  };

  const addFruit = async (fruitName) => {
    try {
      await api.post('/fruits', { name: fruitName });
      fetchFruits();  // Refresh the list after adding a fruit
    } catch (error) {
      console.error("Error adding fruit", error);
    }
  };

  useEffect(() => {
    fetchFruits();
  }, []);

  return (
    <div>
      <h2>Fruits List</h2>
      <ul>
        {fruits.map((fruit, index) => (
          <li key={index}>{fruit.name}</li>
        ))}
      </ul>
      <AddFruitForm addFruit={addFruit} />
    </div>
  );
};

export default FruitList;
```

### AddFruitForm.jsx

```jsx
import React, { useState } from 'react';

const AddFruitForm = ({ addFruit }) => {
  const [fruitName, setFruitName] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (fruitName) {
      addFruit(fruitName);
      setFruitName('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={fruitName}
        onChange={(e) => setFruitName(e.target.value)}
        placeholder="Enter fruit name"
      />
      <button type="submit">Add Fruit</button>
    </form>
  );
};

export default AddFruitForm;
```

### App.jsx

```jsx
import React from 'react';
import './App.css';
import FruitList from './components/Fruits';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Fruit Management App</h1>
      </header>
      <main>
        <FruitList />
      </main>
    </div>
  );
};

export default App;
```

### api.js

```js
import axios from 'axios';

// Create an instance of axios with the base URL
const api = axios.create({
  baseURL: "http://localhost:8000"
});

// Export the Axios instance
export default api;
```

### Run the App

- `npm run dev`
