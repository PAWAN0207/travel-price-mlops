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

        stage("Start API") {
            steps {
                sh '''
                    echo "Starting Flask API..."

                    .venv/bin/python api/app.py > api.log 2>&1 &
                    echo $! > api.pid

                    echo "Waiting for API to start..."

                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if curl -s http://127.0.0.1:5000/health > /dev/null; then
                            echo "API started successfully!"
                            break
                        fi

                        echo "Waiting... ($i/10)"
                        sleep 2
                    done

                    echo "Checking API health..."
                    curl -f http://127.0.0.1:5000/health

                    echo ""
                    echo "API is ready for testing."
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
        always {
            sh '''
                if [ -f api.pid ]; then
                    echo "Stopping Flask API..."
                    kill $(cat api.pid) || true
                fi
            '''
        }

        success {
            echo "CI Pipeline completed successfully!"
        }

        failure {
            echo "CI Pipeline failed."
            sh '''
                if [ -f api.log ]; then
                    echo "========== API LOG =========="
                    cat api.log
                    echo "============================="
                fi
            '''
        }
    }
}