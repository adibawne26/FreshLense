pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.prod.yaml"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -lR monitoring/alertmanager'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cd "$WORKSPACE"

                    rm -rf /opt/freshlense
                    mkdir -p /opt/freshlense
                    cp -a . /opt/freshlense/
                    cd /opt/freshlense

                    cat > .env <<EOF
MONGO_URI=mongodb://mongodb:27017/freshlense
REACT_APP_BACKEND_URL=http://backend:8000
OPENAI_API_KEY=
RESEND_API_KEY=
EOF

                    docker compose -p freshlense -f /opt/freshlense/docker-compose.prod.yaml down --remove-orphans || true

                    docker compose -p freshlense -f /opt/freshlense/docker-compose.prod.yaml pull backend frontend

                    docker compose -p freshlense -f /opt/freshlense/docker-compose.prod.yaml build prometheus

                    docker compose -p freshlense -f /opt/freshlense/docker-compose.prod.yaml up -d
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

                    while true; do
                        STATUS=$(docker inspect -f '{{.State.Health.Status}}' freshlense-mongodb)
                        echo "MongoDB Status: $STATUS"

                        [ "$STATUS" = "healthy" ] && break
                        sleep 5
                    done

                    echo ""
                    echo "==============================="
                    echo "Waiting for Backend..."
                    echo "==============================="

                    while true; do
                        STATUS=$(docker inspect -f '{{.State.Health.Status}}' freshlense-backend)
                        echo "Backend Status: $STATUS"

                        [ "$STATUS" = "healthy" ] && break
                        sleep 5
                    done

                    echo ""
                    echo "==============================="
                    echo "Waiting for Frontend..."
                    echo "==============================="

                    while true; do
                        STATUS=$(docker inspect -f '{{.State.Health.Status}}' freshlense-frontend)
                        echo "Frontend Status: $STATUS"

                        [ "$STATUS" = "healthy" ] && break
                        sleep 5
                    done

                    echo ""
                    echo "=========================================="
                    echo "FreshLense Deployment Successful!"
                    echo "=========================================="

                    docker compose -p freshlense -f /opt/freshlense/docker-compose.prod.yaml ps
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