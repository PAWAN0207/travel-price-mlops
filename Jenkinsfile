pipeline {
    agent any

    environment {
        IMAGE_NAME = "travel-price-api:ci"
        CONTAINER_NAME = "travel-price-api-ci"
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
                    echo "Setting up Python virtual environment..."

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
                    echo "Starting Flask API..."

                    rm -f api.pid api.log

                    .venv/bin/python api/app.py > api.log 2>&1 &
                    echo $! > api.pid

                    echo "API PID: $(cat api.pid)"
                    echo "Waiting for API..."

                    API_READY=false

                    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do

                        if curl -fsS http://127.0.0.1:5000/health > /dev/null 2>&1; then
                            echo "API started successfully!"
                            API_READY=true
                            break
                        fi

                        echo "Waiting... ($i/15)"
                        sleep 2
                    done

                    if [ "$API_READY" != "true" ]; then
                        echo "ERROR: Local API failed to start."

                        echo "========== API LOG =========="
                        cat api.log || true
                        echo "============================="

                        exit 1
                    fi

                    echo "Final API health check..."

                    curl -fsS http://127.0.0.1:5000/health

                    echo ""
                    echo "Local API is healthy."
                '''
            }
        }

        stage("Run API Tests") {
            steps {
                sh '''
                    echo "Running API tests..."

                    .venv/bin/pytest -v tests/test_api.py

                    echo "All API tests passed."
                '''
            }
        }

        stage("Stop Local API") {
            steps {
                sh '''
                    echo "Stopping local Flask API..."

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
                    echo "Building Docker image..."
                    echo "========================================="

                    docker build --pull=false -t travel-price-api:ci .

                    echo ""
                    echo "Docker image built successfully!"

                    docker images travel-price-api:ci
                '''
            }
        }

        stage("Run Docker Container") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Starting Docker container..."
                    echo "========================================="

                    echo "Removing old CI container if present..."

                    docker rm -f travel-price-api-ci 2>/dev/null || true

                    echo "Starting container with a RANDOM FREE HOST PORT..."

                    docker run -d \
                        --name travel-price-api-ci \
                        -p 5000 \
                        travel-price-api:ci

                    echo "Docker container started."

                    echo ""
                    echo "Container status:"
                    docker ps --filter "name=travel-price-api-ci"

                    echo ""
                    echo "Getting dynamically assigned host port..."

                    DOCKER_PORT=$(docker port travel-price-api-ci 5000/tcp | head -n 1 | sed -E 's/.*:([0-9]+).*/\\1/')

                    if [ -z "$DOCKER_PORT" ]; then
                        echo "ERROR: Could not determine Docker host port."

                        docker ps -a --filter "name=travel-price-api-ci"
                        docker logs travel-price-api-ci || true

                        exit 1
                    fi

                    echo "Docker API is mapped to host port: $DOCKER_PORT"

                    echo "$DOCKER_PORT" > docker_api_port.txt

                    echo ""
                    echo "Waiting for Docker API..."

                    API_READY=false

                    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do

                        if curl -fsS "http://127.0.0.1:${DOCKER_PORT}/health" > /dev/null 2>&1; then
                            echo "Docker API started successfully!"
                            API_READY=true
                            break
                        fi

                        echo "Waiting... ($i/15)"
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
                    echo "Docker health check:"

                    curl -fsS "http://127.0.0.1:${DOCKER_PORT}/health"

                    echo ""
                    echo "Docker API is healthy."
                '''
            }
        }

        stage("Test Docker API") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Testing Docker API..."
                    echo "========================================="

                    DOCKER_PORT=$(cat docker_api_port.txt)

                    echo "Using Docker API port: $DOCKER_PORT"

                    echo ""
                    echo "1. Testing health endpoint..."

                    curl -fsS \
                        "http://127.0.0.1:${DOCKER_PORT}/health"

                    echo ""
                    echo ""

                    echo "2. Testing prediction endpoint..."

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
                        "http://127.0.0.1:${DOCKER_PORT}/predict"

                    echo ""
                    echo ""
                    echo "========================================="
                    echo "Docker API tests PASSED!"
                    echo "========================================="
                '''
            }
        }
    }

    post {

        always {
            sh '''
                echo "========================================="
                echo "Running cleanup..."
                echo "========================================="

                if [ -f api.pid ]; then

                    PID=$(cat api.pid)

                    if kill -0 "$PID" 2>/dev/null; then
                        kill "$PID" || true
                    fi

                    rm -f api.pid
                fi

                docker rm -f travel-price-api-ci 2>/dev/null || true

                rm -f docker_api_port.txt

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

                if docker ps -a --format '{{.Names}}' | grep -q '^travel-price-api-ci$'; then
                    echo "========== DOCKER CONTAINER LOG =========="
                    docker logs travel-price-api-ci || true
                    echo "=========================================="
                fi
            '''
        }
    }
}