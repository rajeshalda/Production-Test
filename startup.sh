#!/bin/bash

# Initialize the database
flask db upgrade

# Start Gunicorn
gunicorn --bind=0.0.0.0:8000 "run:app" --timeout 600 