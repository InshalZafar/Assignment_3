pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t selenium-app .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run selenium-app'
            }
        }
    }
}