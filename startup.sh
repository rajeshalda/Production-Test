#!/bin/bash

# Initialize the database
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"

# Start Gunicorn
gunicorn --bind=0.0.0.0:8000 "run:app" 