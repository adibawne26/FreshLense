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

        stage('Docker Credentials Debug') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "========== DEBUG =========="
                        echo "Username: $DOCKER_USER"
                        echo "Password Length: $(printf "%s" "$DOCKER_PASS" | wc -c)"
                        echo "==========================="
                    '''
                }
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" \
                            --password-stdin
                    '''
                }
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
            steps {
                sh '''
                echo "Waiting for MongoDB..."
                until [ "$(docker inspect -f '{{.State.Health.Status}}' freshlense-mongodb)" = "healthy" ]; do
                    sleep 5
                done

                echo "Waiting for Backend..."
                until [ "$(docker inspect -f '{{.State.Health.Status}}' freshlense-backend)" = "healthy" ]; do
                    sleep 5
                done

                echo "Waiting for Frontend..."
                until [ "$(docker inspect -f '{{.State.Health.Status}}' freshlense-frontend)" = "healthy" ]; do
                    sleep 5
                done

                echo ""
                echo "All services are healthy."
                docker compose -f /var/jenkins_home/docker-compose.prod.yaml ps
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment preparation completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}