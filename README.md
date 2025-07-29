# Doctor Advice Web App

A simple Flask-based web application that allows doctors to record and edit patient data, provide advice, prescribe drugs, and export individual reports as PDF.

## Features

- Patient info management
- Medical advice editor
- PDF report download
- Login system (basic)
- Ready for deployment on Render or Railway

## Deploy Instructions

1. Fork this repo or clone locally.
2. Create a virtual environment and install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python app.py
   ```

## Deploy to Render

- Add `Procfile` with:
  ```
  web: gunicorn app:app
  ```

- Add `requirements.txt`, then connect this repo on Render.com.
