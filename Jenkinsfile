pipeline {
    agent any

    environment {
        IMAGE_NAME = "travel-price-api:ci"
        CONTAINER_NAME = "travel-price-api-ci"
        NETWORK_NAME = "jenkins-ci-network"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Setup Python") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Setting up Python environment"
                    echo "========================================="

                    rm -rf .venv

                    python3 -m venv .venv

                    .venv/bin/python --version
                    .venv/bin/pip --version
                '''
            }
        }

        stage("Install Dependencies") {
            steps {
                sh '''
                    echo "Installing Python dependencies..."

                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install --no-cache-dir -r requirements.txt

                    echo "Dependencies installed successfully."
                '''
            }
        }

        stage("Start API") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Starting Local Flask API"
                    echo "========================================="

                    rm -f api.pid api.log

                    .venv/bin/python api/app.py > api.log 2>&1 &
                    echo $! > api.pid

                    echo "API PID: $(cat api.pid)"

                    API_READY=false

                    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do

                        if curl -fsS http://127.0.0.1:5000/health > /dev/null 2>&1; then
                            echo "Local API started successfully!"
                            API_READY=true
                            break
                        fi

                        echo "Waiting for Local API... ($i/15)"
                        sleep 2
                    done

                    if [ "$API_READY" != "true" ]; then
                        echo "ERROR: Local API failed to start."

                        echo "========== API LOG =========="
                        cat api.log || true
                        echo "============================="

                        exit 1
                    fi

                    curl -fsS http://127.0.0.1:5000/health

                    echo ""
                    echo "Local API is healthy."
                '''
            }
        }

        stage("Run API Tests") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Running API Tests"
                    echo "========================================="

                    .venv/bin/pytest -v tests/test_api.py

                    echo "All API tests passed."
                '''
            }
        }

        stage("Stop Local API") {
            steps {
                sh '''
                    echo "Stopping Local Flask API..."

                    if [ -f api.pid ]; then
                        PID=$(cat api.pid)

                        if kill -0 "$PID" 2>/dev/null; then
                            kill "$PID" || true
                            sleep 2
                        fi

                        rm -f api.pid
                    fi

                    echo "Local API stopped."
                '''
            }
        }

        stage("Build Docker Image") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Building Docker Image"
                    echo "========================================="

                    docker build --pull=false -t travel-price-api:ci .

                    echo ""
                    echo "Docker image built successfully."

                    docker images travel-price-api:ci
                '''
            }
        }

        stage("Create CI Network") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Preparing Docker Network"
                    echo "========================================="

                    docker network inspect jenkins-ci-network > /dev/null 2>&1 || \
                    docker network create jenkins-ci-network

                    echo "CI network is ready."
                '''
            }
        }

        stage("Run Docker Container") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Starting Docker API Container"
                    echo "========================================="

                    docker rm -f travel-price-api-ci 2>/dev/null || true

                    docker run -d \
                        --name travel-price-api-ci \
                        --network jenkins-ci-network \
                        travel-price-api:ci

                    echo ""
                    echo "Container started."

                    docker ps --filter "name=travel-price-api-ci"

                    echo ""
                    echo "Waiting for Docker API..."

                    API_READY=false

                    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do

                        if curl -fsS http://travel-price-api-ci:5000/health > /dev/null 2>&1; then
                            echo "Docker API started successfully!"
                            API_READY=true
                            break
                        fi

                        echo "Waiting for Docker API... ($i/15)"
                        sleep 2
                    done

                    if [ "$API_READY" != "true" ]; then
                        echo "ERROR: Docker API failed to start."

                        echo ""
                        echo "========== CONTAINER STATUS =========="

                        docker ps -a --filter "name=travel-price-api-ci"

                        echo ""
                        echo "========== CONTAINER LOGS =========="

                        docker logs travel-price-api-ci || true

                        exit 1
                    fi

                    echo ""
                    echo "Docker API health check:"

                    curl -fsS http://travel-price-api-ci:5000/health

                    echo ""
                    echo "Docker API is healthy."
                '''
            }
        }

        stage("Test Docker API") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Testing Docker API"
                    echo "========================================="

                    echo ""
                    echo "1. Health Endpoint"

                    curl -fsS \
                        http://travel-price-api-ci:5000/health

                    echo ""
                    echo ""

                    echo "2. Prediction Endpoint"

                    curl -fsS \
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
                        http://travel-price-api-ci:5000/predict

                    echo ""
                    echo ""

                    echo "========================================="
                    echo "DOCKER API TESTS PASSED!"
                    echo "========================================="
                '''
            }
        }
    }

    post {

        always {
            sh '''
                echo "========================================="
                echo "Running Cleanup"
                echo "========================================="

                if [ -f api.pid ]; then

                    PID=$(cat api.pid)

                    if kill -0 "$PID" 2>/dev/null; then
                        kill "$PID" || true
                    fi

                    rm -f api.pid
                fi

                docker rm -f travel-price-api-ci 2>/dev/null || true

                echo "Cleanup completed."
            '''
        }

        success {
            echo "========================================="
            echo "CI/CD PIPELINE SUCCESSFUL!"
            echo "========================================="
        }

        failure {
            echo "========================================="
            echo "CI/CD PIPELINE FAILED!"
            echo "========================================="

            sh '''
                if [ -f api.log ]; then
                    echo "========== LOCAL API LOG =========="
                    cat api.log
                    echo "=================================="
                fi
            '''
        }
    }
}