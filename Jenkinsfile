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

                    echo "Waiting for API..."

                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if curl -s http://127.0.0.1:5000/health > /dev/null; then
                            echo "API started successfully!"
                            break
                        fi

                        echo "Waiting... ($i/10)"
                        sleep 2
                    done

                    curl -f http://127.0.0.1:5000/health
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

        stage("Stop Local API") {
            steps {
                sh '''
                    if [ -f api.pid ]; then
                        kill $(cat api.pid) || true
                    fi
                '''
            }
        }

        stage("Build Docker Image") {
            steps {
                sh '''
                    docker build -t travel-price-api:ci .
                '''
            }
        }

        stage("Run Docker Container") {
            steps {
                sh '''
                    docker rm -f travel-price-api-ci 2>/dev/null || true

                    docker run -d \
                        --name travel-price-api-ci \
                        -p 5001:5000 \
                        travel-price-api:ci

                    echo "Waiting for Docker API..."

                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        if curl -s http://127.0.0.1:5001/health > /dev/null; then
                            echo "Docker API started successfully!"
                            break
                        fi

                        echo "Waiting... ($i/10)"
                        sleep 2
                    done
                '''
            }
        }

        stage("Test Docker API") {
            steps {
                sh '''
                    echo "Testing Docker health endpoint..."
                    curl -f http://127.0.0.1:5001/health

                    echo ""
                    echo "Testing Docker prediction endpoint..."

                    curl -f \
                        -X POST \
                        -H "Content-Type: application/json" \
                        -d '{
                            "from": "Recife (PE)",
                            "to": "Florianopolis (SC)",
                            "flightType": "firstClass",
                            "time": 1.76,
                            "distance": 676.53,
                            "agency": "FlyingDrops"
                        }' \
                        http://127.0.0.1:5001/predict

                    echo ""
                    echo "Docker API tests passed!"
                '''
            }
        }
    }

    post {
        always {
            sh '''
                if [ -f api.pid ]; then
                    kill $(cat api.pid) || true
                fi

                docker rm -f travel-price-api-ci 2>/dev/null || true
            '''
        }

        success {
            echo "CI/CD Pipeline completed successfully!"
        }

        failure {
            echo "CI/CD Pipeline failed."

            if [ -f api.log ]; then
                echo "========== API LOG =========="
                cat api.log
                echo "============================="
            fi
        }
    }
}