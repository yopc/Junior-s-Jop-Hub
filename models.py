from extensions import db, ma

# Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100))
    url = db.Column(db.String(500))
    date_scraped = db.Column(db.Date)
    matched = db.Column(db.Boolean, default=False)

# Job schema for serialization
class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
        fields = ('id', 'title', 'company', 'location', 'url', 'date_scraped', 'matched')

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
