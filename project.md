# 🌍 Tourism Explorer Web Application

### DevOps & Cloud Deployment Project (From Scratch)

---

# 1. 📌 Project Overview

**Tourism Explorer** is a web-based application designed to help users explore tourist destinations, create travel plans, and share reviews.

This project is built to demonstrate:

* Full-stack web development
* Containerization using Docker
* Cloud deployment using AWS EC2
* CI/CD automation using Jenkins

The system is intentionally designed to be simple yet scalable, making it ideal for DevOps learning and academic evaluation.

---

# 2. 🎯 Objectives

This project aims to:

* Understand Docker containerization
* Deploy applications on AWS EC2 (IaaS)
* Automate deployment using Jenkins (CI/CD)
* Work with databases in containerized environments
* Build a modular web application with CRUD functionality

---

# 3. 🛠️ Technology Stack

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3
* Bootstrap 5

### Database

* SQLite (Phase 1)
* MySQL (Phase 2 - Docker)

### DevOps Tools

* Docker
* Docker Compose
* Jenkins

### Cloud

* AWS EC2

---

# 4. 🧱 System Architecture

User
↓
Browser
↓
Flask Application
↓
Database

---

# 5. 📂 Project Structure

```
tourism-explorer/
│
├── app.py
├── application.py
├── models.py
├── forms.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── templates/
├── static/
│
└── instance/
```

---

# 6. 🔐 Module 1 — User Authentication

### Features:

* Register user
* Login
* Logout
* Session management
* Update profile
* Delete account

---

# 7. 🌍 Module 2 — Destination Management

### Features:

* View destinations
* Add destination
* Edit destination
* Delete destination
* Search destinations
* Filter destinations

---

# 8. 🧳 Module 3 — Reviews & Travel Plans

### Features:

* Add review
* View reviews
* Edit review
* Delete review
* Create travel plan
* Add destination to plan
* Remove destination from plan
* Delete travel plan

---

# 9. 📊 Use Case Summary

Total Use Cases: **20**

Actors:

* User
* (Optional) Admin

---

# 10. ⚙️ Phase 1 — Local Development

### Run Application:

```bash
python application.py
```

Access:

```
http://localhost:5000
```

---

# 11. 🐳 Phase 2 — Dockerization

## Dockerfile

```dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "application.py"]
```

---

## Build Image

```bash
docker build -t yourusername/tourism-app .
```

---

## Run Container

```bash
docker run -p 5000:5000 yourusername/tourism-app
```

---

# 12. 📦 Docker Compose (Multi-Container Setup)

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: rootpassword
      DB_NAME: flask_app_db
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: flask_app_db
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

---

# 13. ☁️ Phase 3 — AWS EC2 Deployment

### Steps:

1. Launch EC2 (Ubuntu 22.04)
2. Install Docker:

```bash
sudo apt update
sudo apt install docker.io -y
```

3. Clone project:

```bash
git clone YOUR_REPO_LINK
cd tourism-explorer
```

4. Run:

```bash
docker-compose up -d --build
```

Access:

```
http://EC2-IP:5000
```

---

# 14. 🔄 Phase 4 — CI/CD using Jenkins

### Steps:

1. Install Jenkins on EC2
2. Connect GitHub repository
3. Create Pipeline

---

## Jenkins Pipeline Script

```groovy
pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'YOUR_GITHUB_REPO'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t tourism-app .'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }
}
```

---

# 15. 🔗 GitHub Webhook

Payload URL:

```
http://EC2-IP:8080/github-webhook/
```

---

# 16. 📈 Deployment Results

| Part            | Port | Status      |
| --------------- | ---- | ----------- |
| Manual (Docker) | 5000 | Running     |
| CI/CD (Jenkins) | 8081 | Auto Deploy |

---

# 17. 🧠 Key Learnings

* Containerization ensures consistency
* Docker Compose manages multi-container apps
* AWS EC2 provides scalable infrastructure
* Jenkins automates deployment
* CI/CD reduces manual effort

---

# 18. ✅ Conclusion

This project demonstrates a complete DevOps pipeline from development to deployment. It highlights the integration of modern tools such as Docker, AWS, and Jenkins to achieve automated and scalable application delivery.

---

