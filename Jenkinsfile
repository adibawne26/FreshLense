pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "adityabawne37/freshlense-backend:latest"
        FRONTEND_IMAGE = "adityabawne37/freshlense-frontend:latest"
        NETWORK = "freshlense-network"
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
                    echo "Stopping old containers..."

                    docker rm -f freshlense-backend || true
                    docker rm -f freshlense-frontend || true

                    echo "Starting Backend..."

                    docker run -d \
                        --name freshlense-backend \
                        --network ${NETWORK} \
                        -p 8000:8000 \
                        --restart unless-stopped \
                        -e MONGO_URI=mongodb://freshlense-mongodb:27017/freshlense \
                        ${BACKEND_IMAGE}

                    echo "Starting Frontend..."

                    docker run -d \
                        --name freshlense-frontend \
                        --network ${NETWORK} \
                        -p 3000:3000 \
                        --restart unless-stopped \
                        -e REACT_APP_BACKEND_URL=http://freshlense-backend:8000 \
                        ${FRONTEND_IMAGE}
                '''
            }
        }

        stage('Verify Deployment') {

            options {
                timeout(time: 3, unit: 'MINUTES')
            }

            steps {
                sh '''
                    echo "================================"
                    echo "Checking MongoDB..."
                    echo "================================"

                    docker ps | grep freshlense-mongodb

                    echo ""
                    echo "================================"
                    echo "Waiting for Backend..."
                    echo "================================"

                    while true; do
                        STATUS=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}starting{{end}}' freshlense-backend)
                        echo "Backend Status: $STATUS"

                        [ "$STATUS" = "healthy" ] && break
                        sleep 5
                    done

                    echo ""
                    echo "================================"
                    echo "Waiting for Frontend..."
                    echo "================================"

                    while true; do
                        STATUS=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}starting{{end}}' freshlense-frontend)
                        echo "Frontend Status: $STATUS"

                        [ "$STATUS" = "healthy" ] && break
                        sleep 5
                    done

                    echo ""
                    echo "=========================================="
                    echo " FreshLense Deployment Successful!"
                    echo "=========================================="

                    docker ps
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