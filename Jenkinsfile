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

        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ['ec2-deploy-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@40.192.105.6 "
                            cd ~/FreshLense &&
                            docker compose -f docker-compose.ec2.yaml pull &&
                            docker compose -f docker-compose.ec2.yaml up -d &&
                            docker image prune -f
                        "
                    """
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sshagent(credentials: ['ec2-deploy-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@40.192.105.6 "
                            docker ps &&
                            curl http://localhost:8000/health
                        "
                    """
                }
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