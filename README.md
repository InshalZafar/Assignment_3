# Tourism Web App - Selenium Testing Assignment

## Features
- User Registration & Login
- Destination Management
- Travel Plans

## Selenium Testing
- 15 automated test cases
- Uses headless Chrome
- Covers authentication, navigation, and UI

## How to Run Locally

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run app
python app.py

### 3. Run tests
pytest -v

## Docker Usage

Build:
docker build -t selenium-app .

Run:
docker run selenium-app

## Jenkins Pipeline
A Jenkinsfile is included to automate:
- Build Docker image
- Run Selenium tests

## Notes
- CSRF disabled for testing
- Tests designed to be stable and reproducible