pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.prod.yaml"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cd "$WORKSPACE"

                    echo "====================================="
                    echo "Pulling latest images..."
                    echo "====================================="

                    docker compose -f ${COMPOSE_FILE} pull

                    echo "====================================="
                    echo "Starting FreshLense..."
                    echo "====================================="

                    docker compose -f ${COMPOSE_FILE} up -d --remove-orphans
                '''
            }
        }

        stage('Verify Deployment') {

            options {
                timeout(time: 5, unit: 'MINUTES')
            }

            steps {
                sh '''
                    echo ""
                    echo "==============================="
                    echo "Waiting for MongoDB..."
                    echo "==============================="

                    until [ "$(docker inspect -f '{{.State.Health.Status}}' freshlense-mongodb)" = "healthy" ]; do
                        docker inspect -f '{{.State.Health.Status}}' freshlense-mongodb
                        sleep 5
                    done

                    echo ""
                    echo "==============================="
                    echo "Waiting for Backend..."
                    echo "==============================="

                    until [ "$(docker inspect -f '{{.State.Health.Status}}' freshlense-backend)" = "healthy" ]; do
                        docker inspect -f '{{.State.Health.Status}}' freshlense-backend
                        sleep 5
                    done

                    echo ""
                    echo "==============================="
                    echo "Waiting for Frontend..."
                    echo "==============================="

                    until [ "$(docker inspect -f '{{.State.Health.Status}}' freshlense-frontend)" = "healthy" ]; do
                        docker inspect -f '{{.State.Health.Status}}' freshlense-frontend
                        sleep 5
                    done

                    echo ""
                    echo "=========================================="
                    echo "FreshLense Deployment Successful!"
                    echo "=========================================="

                    docker compose -f ${COMPOSE_FILE} ps
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