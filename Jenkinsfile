pipeline {
    agent any

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Setup Python") {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python --version
                    .venv/bin/pip --version
                '''
            }
        }

        stage("Install Dependencies") {
            steps {
                sh '''
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage("Run API Tests") {
            steps {
                sh '''
                    .venv/bin/pytest -v tests/test_api.py
                '''
            }
        }
    }

    post {
        success {
            echo "CI Pipeline completed successfully!"
        }

        failure {
            echo "CI Pipeline failed."
        }
    }
}
