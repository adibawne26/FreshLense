pipeline {
    agent any

    environment {
        DOCKER_USERNAME = "adityabawne37"
        BACKEND_IMAGE = "adityabawne37/freshlense-backend:latest"
        FRONTEND_IMAGE = "adityabawne37/freshlense-frontend:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
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

        stage('Pull Images') {
            steps {
                sh """
                docker pull ${BACKEND_IMAGE}
                docker pull ${FRONTEND_IMAGE}
                """
            }
        }

        stage('Verify Images') {
            steps {
                sh 'docker images | grep freshlense'
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