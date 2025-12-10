from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from dotenv import load_dotenv
from extensions import db, ma


load_dotenv()

app = Flask(__name__)
CORS(app) 


DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "jop_hub")


app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  



# Initialize extensions
db.init_app(app)
ma.init_app(app)

# Import models after initializing db to avoid circular imports
from models import Job, job_schema, jobs_schema

# Routes
@app.route("/")
def index():
    return jsonify({"message": "Flask app connected to MySQL!", "status": "success"})

@app.route("/jobs", methods=["GET"])
def get_jobs():
    """Fetch all jobs from the database."""
    try:
        all_jobs = Job.query.all()
        result = jobs_schema.dump(all_jobs)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import request

# CREATE a new job
@app.route("/jobs", methods=["POST"])
def create_jobs():
    data = request.get_json()  # Could be a dict (single) or list (multiple)
    try:
        if isinstance(data, list):  # Multiple jobs
            new_jobs = []
            for item in data:
                job = Job(
                    title=item["title"],
                    company=item["company"],
                    location=item["location"]
                )
                db.session.add(job)
                new_jobs.append(job)
            db.session.commit()
            return jobs_schema.jsonify(new_jobs), 201

        elif isinstance(data, dict):  # Single job
            job = Job(
                title=data["title"],
                company=data["company"],
                location=data["location"]
            )
            db.session.add(job)
            db.session.commit()
            return job_schema.jsonify(job), 201

        else:
            return jsonify({"error": "Invalid input format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# READ a single job by ID
@app.route("/jobs/<int:id>", methods=["GET"])
def get_job(id):
    job = Job.query.get_or_404(id)
    return jobs_schema.jsonify(job)

# UPDATE a job by ID
@app.route("/jobs/<int:id>", methods=["PUT"])
def update_job(id):
    job = Job.query.get_or_404(id)
    data = request.get_json()
    try:
        job.title = data.get("title", job.title)
        job.company = data.get("company", job.company)
        job.location = data.get("location", job.location)
        db.session.commit()
        return jobs_schema.jsonify(job)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE a job by ID
@app.route("/jobs/<int:id>", methods=["DELETE"])
def delete_job(id):
    job = Job.query.get_or_404(id)
    try:
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": f"Job {id} deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
