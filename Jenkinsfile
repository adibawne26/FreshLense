pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "adityabawne37/freshlense-backend:latest"
        FRONTEND_IMAGE = "adityabawne37/freshlense-frontend:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Pull Latest Images') {
            steps {
                retry(3) {
                    sh '''
                    docker pull ${BACKEND_IMAGE}
                    docker pull ${FRONTEND_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                cd /var/jenkins_home

                docker compose -f docker-compose.prod.yaml down
                docker compose -f docker-compose.prod.yaml up -d
                '''
            }
        }

        stage('Verify Deployment') {

            options {
                timeout(time: 3, unit: 'MINUTES')
            }

            steps {
                sh '''
                echo "==============================="
                echo "Waiting for MongoDB..."
                echo "==============================="

                while true; do
                    STATUS=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' freshlense-mongodb)
                    echo "MongoDB Status: $STATUS"

                    [ "$STATUS" = "healthy" ] && break
                    sleep 5
                done

                echo ""
                echo "==============================="
                echo "Waiting for Backend..."
                echo "==============================="

                while true; do
                    STATUS=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' freshlense-backend)
                    echo "Backend Status: $STATUS"

                    [ "$STATUS" = "healthy" ] && break
                    sleep 5
                done

                echo ""
                echo "==============================="
                echo "Waiting for Frontend..."
                echo "==============================="

                while true; do
                    STATUS=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' freshlense-frontend)
                    echo "Frontend Status: $STATUS"

                    [ "$STATUS" = "healthy" ] && break
                    sleep 5
                done

                echo ""
                echo "=========================================="
                echo "FreshLense Deployment Successful!"
                echo "All services are healthy."
                echo "=========================================="

                docker compose -f /var/jenkins_home/docker-compose.prod.yaml ps
                '''
            }
        }
    }

    post {

        success {
            echo 'FreshLense deployed successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}