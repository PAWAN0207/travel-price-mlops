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

                    echo "Final API health check..."
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
                        kill $(cat api.pid) 2>/dev/null || true
                        rm -f api.pid
                    fi
                '''
            }
        }

        stage("Build Docker Image") {
            steps {
                sh '''
                    echo "Building Docker image..."

                    docker build -t travel-price-api:ci .

                    echo "Docker image built successfully!"

                    docker images travel-price-api:ci
                '''
            }
        }

        stage("Run Docker Container") {
            steps {
                sh '''
                    echo "Removing previous CI container if it exists..."

                    docker rm -f travel-price-api-ci 2>/dev/null || true

                    echo "Starting Docker container..."

                    docker run -d \
                        --name travel-price-api-ci \
                        -p 5003:5000 \
                        travel-price-api:ci

                    echo "Docker container started."

                    echo "Waiting for Docker API..."

                    API_READY=false

                    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do

                        if curl -s http://127.0.0.1:5003/health > /dev/null; then
                            echo "Docker API started successfully!"
                            API_READY=true
                            break
                        fi

                        echo "Waiting... ($i/20)"
                        sleep 2
                    done

                    echo "Checking Docker container status..."

                    docker ps -a \
                        --filter "name=travel-price-api-ci" \
                        --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"

                    if [ "$API_READY" != "true" ]; then
                        echo "Docker API failed to become ready."
                        echo "========== DOCKER CONTAINER LOGS =========="
                        docker logs travel-price-api-ci || true
                        echo "==========================================="
                        exit 1
                    fi

                    echo "Final Docker health check..."

                    curl -f http://127.0.0.1:5003/health
                '''
            }
        }

        stage("Test Docker API") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Testing Docker health endpoint"
                    echo "========================================="

                    curl -f http://127.0.0.1:5003/health

                    echo ""
                    echo "========================================="
                    echo "Testing Docker prediction endpoint"
                    echo "========================================="

                    curl -f \
                        -X POST \
                        -H "Content-Type: application/json" \
                        -d '{
                            "from": "Recife (PE)",
                            "to": "Florianopolis (SC)",
                            "flightType": "firstClass",
                            "time": 1.76,
                            "distance": 676.53,
                            "agency": "FlyingDrops",
                            "year": 2026,
                            "month": 8,
                            "day": 28,
                            "day_of_week": 5
                        }' \
                        http://127.0.0.1:5003/predict

                    echo ""
                    echo ""
                    echo "Docker API tests passed successfully!"
                '''
            }
        }
    }

    post {

        always {
            sh '''
                echo "Running cleanup..."

                if [ -f api.pid ]; then
                    kill $(cat api.pid) 2>/dev/null || true
                    rm -f api.pid
                fi

                docker rm -f travel-price-api-ci 2>/dev/null || true

                echo "Cleanup completed."
            '''
        }

        success {
            echo "========================================="
            echo "CI/CD PIPELINE COMPLETED SUCCESSFULLY!"
            echo "========================================="
        }

        failure {
            echo "========================================="
            echo "CI/CD PIPELINE FAILED."
            echo "========================================="

            sh '''
                if [ -f api.log ]; then
                    echo "========== LOCAL API LOG =========="
                    cat api.log
                    echo "==================================="
                fi
            '''
        }
    }
}