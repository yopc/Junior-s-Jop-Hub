# Job Hub Backend

This is the Flask backend for the Job Hub application.

## Prerequisites

- Python 3.8+
- MySQL Server

## Setup

1.  **Clone the repository** (if not already done).
2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    # source venv/bin/activate  # macOS/Linux
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    - Ensure `.env` exists and contains your database credentials:
      ```
      DB_USER=root
      DB_PASSWORD=your_password
      DB_HOST=localhost
      DB_NAME=jop_hub
      ```

## Database Initialization

You only need to do this once.

1.  **Create the Database**:
    ```bash
    python create_db.py
    ```
2.  **Create Tables**:
    ```bash
    python init_db.py
    ```

## Running the Server

Start the Flask application:

```bash
python app.py
```

The server will start at `http://localhost:5000`.

### API Endpoints

-   `GET /`: Health check. Returns `{"message": "Flask app connected to MySQL!", "status": "success"}`.
-   `GET /jobs`: Returns a list of all jobs in the database.
