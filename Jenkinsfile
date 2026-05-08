// Aurelia CI pipeline
//
// Triggered by GitHub push on InshalZafar/Assignment_3.
// 1. Builds the app Docker image
// 2. Brings up the containerized deployment (app + db)
// 3. Clones the dedicated test repo and builds the Selenium image
// 4. Runs the 40-case Selenium suite against the deployed app
// 5. Publishes JUnit + HTML report
// 6. Emails the test results to the collaborator who pushed
//
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        APP_IMAGE  = "aurelia-app:${env.BUILD_NUMBER}"
        TEST_IMAGE = "aurelia-tests:${env.BUILD_NUMBER}"
        NETWORK    = "aurelia-net"
        APP_PORT   = "5000"
        TEST_REPO  = "https://github.com/InshalZafar/Assignment_3_tests.git"
    }

    stages {
        stage('Checkout app') {
            steps {
                checkout scm
                script {
                    env.PUSHER_EMAIL = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=format:'%ae'"
                    ).trim()
                    env.PUSHER_NAME = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=format:'%an'"
                    ).trim()
                    env.COMMIT_MSG = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=format:'%s'"
                    ).trim()
                }
                echo "Build triggered by ${env.PUSHER_NAME} <${env.PUSHER_EMAIL}>"
                echo "Commit: ${env.COMMIT_MSG}"
            }
        }

        stage('Build app image') {
            steps {
                sh 'docker build -t $APP_IMAGE -f Dockerfile.app .'
            }
        }

        stage('Deploy app + db') {
            steps {
                sh '''
                    set -e
                    docker network inspect $NETWORK >/dev/null 2>&1 || docker network create $NETWORK
                    docker rm -f aurelia-db aurelia-app 2>/dev/null || true

                    docker run -d --name aurelia-db --network $NETWORK \
                        -e MYSQL_ROOT_PASSWORD=rootpassword \
                        -e MYSQL_DATABASE=flask_app_db \
                        mysql:8.0

                    echo "Waiting for MySQL to accept connections..."
                    for i in $(seq 1 60); do
                        docker exec aurelia-db mysqladmin -uroot -prootpassword ping --silent 2>/dev/null && break
                        sleep 2
                    done
                    # Even after ping succeeds the user/db init isn't always finished
                    sleep 5

                    docker run -d --name aurelia-app --network $NETWORK \
                        --restart on-failure:5 \
                        -p $APP_PORT:5000 \
                        -e DB_HOST=aurelia-db \
                        -e DB_USER=root \
                        -e DB_PASSWORD=rootpassword \
                        -e DB_NAME=flask_app_db \
                        $APP_IMAGE

                    echo "Waiting for Aurelia to come up..."
                    for i in $(seq 1 60); do
                        if docker inspect -f '{{.State.Running}}' aurelia-app 2>/dev/null | grep -q true; then
                            if docker exec aurelia-app curl -sf http://localhost:5000/ >/dev/null 2>&1; then
                                break
                            fi
                        fi
                        sleep 2
                    done

                    echo "App container status:"
                    docker ps --filter name=aurelia-app
                    echo "App container last logs:"
                    docker logs --tail 30 aurelia-app || true

                    echo "Seeding database..."
                    docker exec aurelia-app python populate_db.py
                '''
            }
        }

        stage('Checkout tests') {
            steps {
                dir('test-repo') {
                    git branch: 'main',
                        credentialsId: 'github-pat',
                        url: env.TEST_REPO
                }
            }
        }

        stage('Build test image') {
            steps {
                dir('test-repo') {
                    sh 'docker build -t $TEST_IMAGE .'
                }
            }
        }

        stage('Run Selenium tests') {
            steps {
                sh '''
                    set -e
                    mkdir -p test-results
                    chmod 777 test-results
                    docker run --rm --network $NETWORK \
                        -e BASE_URL=http://aurelia-app:5000 \
                        -v $WORKSPACE/test-results:/tests \
                        $TEST_IMAGE \
                        pytest -v tests/ \
                            --junitxml=/tests/results.xml \
                            --html=/tests/report.html \
                            --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results/results.xml'

            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'test-results',
                reportFiles: 'report.html',
                reportName: 'Selenium Report'
            ])

            script {
                def status   = currentBuild.currentResult
                def emoji    = status == 'SUCCESS' ? '✓' : '✗'
                def color    = status == 'SUCCESS' ? '#4ade80' : '#ff6b6b'
                def to       = env.PUSHER_EMAIL ?: 'qasimalik@gmail.com'

                emailext(
                    subject: "[Aurelia CI] Build #${env.BUILD_NUMBER} — ${status} ${emoji}",
                    to: to,
                    mimeType: 'text/html',
                    attachmentsPattern: 'test-results/report.html, test-results/results.xml',
                    body: """
<!DOCTYPE html>
<html><body style="font-family:Inter,system-ui,sans-serif;max-width:640px;margin:auto;padding:20px;background:#0a0e27;color:#f4f1e8;">
  <h2 style="font-family:Playfair Display,Georgia,serif;color:#d4af37;border-bottom:1px solid rgba(212,175,55,0.3);padding-bottom:8px;">
    Aurelia · Selenium CI
  </h2>
  <p style="font-size:1.4rem;color:${color};font-weight:600;">${emoji} ${status}</p>
  <table style="width:100%;font-size:0.9rem;color:#9ba3c4;">
    <tr><td style="padding:6px 0;">Build</td>
        <td><a style="color:#d4af37;" href="${env.BUILD_URL}">#${env.BUILD_NUMBER}</a></td></tr>
    <tr><td style="padding:6px 0;">Triggered by</td>
        <td style="color:#f4f1e8;">${env.PUSHER_NAME} &lt;${env.PUSHER_EMAIL}&gt;</td></tr>
    <tr><td style="padding:6px 0;">Commit</td>
        <td style="color:#f4f1e8;">${env.COMMIT_MSG ?: '—'}</td></tr>
    <tr><td style="padding:6px 0;">SHA</td>
        <td style="color:#f4f1e8;font-family:monospace;">${env.GIT_COMMIT}</td></tr>
  </table>
  <p style="margin-top:24px;">
    <a href="${env.BUILD_URL}Selenium_20Report/" style="background:#d4af37;color:#0a0e27;padding:10px 18px;border-radius:999px;text-decoration:none;font-weight:600;">View HTML Report →</a>
    &nbsp;
    <a href="${env.BUILD_URL}console" style="color:#9ba3c4;text-decoration:none;">Console output</a>
  </p>
  <p style="font-size:0.78rem;color:#9ba3c4;margin-top:30px;border-top:1px solid rgba(212,175,55,0.2);padding-top:12px;">
    Aurelia · automated build email
  </p>
</body></html>
                    """
                )
            }
        }

        failure {
            echo "Build failed — see emailed report for details."
        }
    }
}
