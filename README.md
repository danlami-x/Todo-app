FastAPI To-Do App

A simple To-Do app built with FastAPI to manage tasks in memory.

Features

- Add new tasks
- Get all tasks
- Delete tasks
- Mark tasks as completed

Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic

Setup & Run

1. Clone the repo:

bash
git clone https://github.com/dev-danlami/todo-app.git
cd todo-app


2. Create and activate a virtual environment (optional but recommended):

bash
python -m venv venv
source venv/bin/activate 


3. Install dependencies:

bash
pip install -r requirements.txt


4. Run the app:

bash
uvicorn main:app --host 0.0.0.0 --port 8002 --reload


5. Open your browser and go to `http://localhost:8002`

API Endpoints

- `GET /tasks` — Get all tasks
- `POST /tasks` — Add a new task
- `DELETE /tasks/{task_id}` — Delete a task by ID
- `PUT /tasks/{task_id}` — Update a task (e.g., mark complete)

Docker

Build the image:

bash
docker build -t todo-app .


Run the container:

bash
docker run -p 8002:8002 todo-app


Contact

Danlami Bethel  
Email: betheldanlami@gmail.com  
GitHub: [dev-danlami](https://github.com/dev-danlami)
