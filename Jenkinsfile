pipeline {
    agent any

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Install Dependencies") {
            steps {
                sh "python --version"
                sh "pip install --no-cache-dir -r requirements.txt"
            }
        }

        stage("Run API Tests") {
            steps {
                sh "pytest -v tests/test_api.py"
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
