Here's a `README.md` to help guide users on how to launch the API backend and the React frontend locally:

---

# Traveling Salesman Problem Visualizer

This project consists of a Genetic Algorithm (GA), Simulated Annealing (SA) and Best First Search powered API backend built with Flask, and a React frontend for visualizing the results. This guide will walk you through setting up the project locally.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 14+**
- **npm or yarn**

## Setting Up the Backend

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Backend

Start the Flask API server:

```bash
python -m app.app
```

The API server should now be running on `http://127.0.0.1:5000`.

### 5. (Optional) Run the Flask API in Development Mode

If you want to enable auto-reloading and other development features, run:

```bash
FLASK_APP=app.app FLASK_ENV=development flask run
```

## Setting Up the Frontend

### 1. Navigate to the Frontend Directory

```bash
cd frontend  # Replace 'frontend' with your frontend directory's name if different
```

### 2. Install Frontend Dependencies

If you're using npm:

```bash
npm install
```

Or if you're using yarn:

```bash
yarn install
```

### 3. Start the React Frontend

If you're using npm:

```bash
npm start
```

Or if you're using yarn:

```bash
yarn start
```

The frontend should now be running on `http://localhost:3000`.

## Accessing the Application

- **API Backend**: `http://127.0.0.1:5000`
- **React Frontend**: `http://localhost:3000`

## Troubleshooting

- **Port Conflicts**: Ensure the ports `5000` (backend) and `3000` (frontend) are available on your machine.
- **Environment Variables**: Double-check that all required environment variables are correctly set in your `.env` files.