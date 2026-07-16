pipeline {
    agent any

    environment {
        PROJECT_NAME = "freshlense"
        WORK_DIR = "${WORKSPACE}"
        COMPOSE_FILE = "${WORKSPACE}/docker-compose.prod.yaml"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                sh '''
                    echo "===== Workspace ====="
                    pwd
                    echo "$WORKSPACE"

                    echo "===== Monitoring Files ====="
                    find monitoring -maxdepth 2 -ls

                    ls -l monitoring/alertmanager
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -e

                    cd "$WORKSPACE"

                    cat > .env <<EOF
MONGO_URI=mongodb://mongodb:27017/freshlense
REACT_APP_BACKEND_URL=http://backend:8000
OPENAI_API_KEY=
RESEND_API_KEY=
EOF

                    echo "===== Docker Compose Version ====="
                    docker compose version

                    echo "===== Compose Configuration ====="
                    docker compose \
                        --project-directory "$WORKSPACE" \
                        -f "$COMPOSE_FILE" config >/dev/null

                    docker compose \
                        --project-directory "$WORKSPACE" \
                        -p "$PROJECT_NAME" \
                        -f "$COMPOSE_FILE" \
                        down --remove-orphans || true

                    docker compose \
                        --project-directory "$WORKSPACE" \
                        -p "$PROJECT_NAME" \
                        -f "$COMPOSE_FILE" \
                        pull backend frontend

                    docker compose \
                        --project-directory "$WORKSPACE" \
                        -p "$PROJECT_NAME" \
                        -f "$COMPOSE_FILE" \
                        build prometheus

                    docker compose \
                        --project-directory "$WORKSPACE" \
                        -p "$PROJECT_NAME" \
                        -f "$COMPOSE_FILE" \
                        up -d
                '''
            }
        }

        stage('Verify Deployment') {
            options {
                timeout(time: 5, unit: 'MINUTES')
            }

            steps {
                sh '''
                    wait_for_health () {
                        CONTAINER=$1

                        while true
                        do
                            STATUS=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}' "$CONTAINER" 2>/dev/null || true)

                            echo "$CONTAINER : $STATUS"

                            if [ "$STATUS" = "healthy" ] || [ "$STATUS" = "running" ]; then
                                break
                            fi

                            sleep 5
                        done
                    }

                    wait_for_health freshlense-mongodb
                    wait_for_health freshlense-backend
                    wait_for_health freshlense-frontend

                    echo ""
                    echo "======================================"
                    echo "FreshLense Deployment Successful"
                    echo "======================================"

                    docker compose \
                        --project-directory "$WORKSPACE" \
                        -p "$PROJECT_NAME" \
                        -f "$COMPOSE_FILE" \
                        ps
                '''
            }
        }
    }

    post {

        success {
            echo 'FreshLense deployed successfully!'
        }

        failure {
            sh '''
                echo "===== Docker Containers ====="
                docker ps -a || true

                echo ""
                echo "===== Docker Compose Logs ====="
                docker compose \
                    --project-directory "$WORKSPACE" \
                    -p "$PROJECT_NAME" \
                    -f "$COMPOSE_FILE" \
                    logs --tail=50 || true
            '''

            echo 'Pipeline failed.'
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}