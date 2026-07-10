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
                sh '''
                docker pull ${BACKEND_IMAGE}
                docker pull ${FRONTEND_IMAGE}
                '''
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
                echo "Waiting for MongoDB..."

                until [ "$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' freshlense-mongodb)" = "healthy" ]; do
                    sleep 5
                done

                echo "MongoDB is healthy."

                echo "Waiting for Backend..."

                until [ "$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' freshlense-backend)" = "healthy" ]; do
                    sleep 5
                done

                echo "Backend is healthy."

                echo "Waiting for Frontend..."

                until [ "$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' freshlense-frontend)" = "healthy" ]; do
                    sleep 5
                done

                echo "Frontend is healthy."

                echo ""
                echo "All services are healthy."

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