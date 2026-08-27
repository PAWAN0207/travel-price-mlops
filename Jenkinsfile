pipeline {
    agent any

    environment {
        IMAGE_NAME = "travel-price-api"
        IMAGE_TAG = "ci"
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
                    echo "========================================="
                    echo "Installing Python dependencies"
                    echo "========================================="

                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install --no-cache-dir -r requirements.txt

                    echo "Dependencies installed successfully."
                '''
            }
        }

        stage("Start Local API") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Starting Local Flask API"
                    echo "========================================="

                    rm -f api.pid api.log

                    nohup .venv/bin/python api/app.py > api.log 2>&1 &

                    API_PID=$!
                    echo $API_PID > api.pid

                    echo "API PID: $API_PID"
                    echo "Waiting for Local API..."

                    API_READY=false

                    for i in $(seq 1 20); do

                        if curl -fsS http://127.0.0.1:5000/health > /dev/null 2>&1; then
                            echo "Local API started successfully!"
                            API_READY=true
                            break
                        fi

                        echo "Waiting for Local API... ($i/20)"
                        sleep 2
                    done

                    if [ "$API_READY" != "true" ]; then
                        echo "ERROR: Local API failed to start."

                        echo "========== LOCAL API LOG =========="
                        cat api.log || true
                        echo "==================================="

                        exit 1
                    fi

                    echo "Final Local API health check:"
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
                    echo "========================================="
                    echo "Stopping Local Flask API"
                    echo "========================================="

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

                    docker build --pull=false \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    echo ""
                    echo "Docker image built successfully."

                    docker images ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage("Run Docker Container") {
            steps {
                sh '''
                    echo "========================================="
                    echo "Starting Docker API Container"
                    echo "========================================="

                    echo "Removing old container if present..."

                    docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

                    echo "Starting Docker container..."

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 127.0.0.1::5000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    echo ""
                    echo "Docker container started."

                    echo "Container status:"

                    docker ps \
                        --filter "name=${CONTAINER_NAME}" \
                        --format "table {{.ID}}\\t{{.Status}}\\t{{.Ports}}\\t{{.Names}}"

                    echo ""
                    echo "Getting dynamically assigned host port..."

                    DOCKER_PORT=$(docker port ${CONTAINER_NAME} 5000/tcp | head -n 1 | sed -E 's/.*:([0-9]+).*/\\1/')

                    if [ -z "$DOCKER_PORT" ]; then
                        echo "ERROR: Could not determine Docker host port."

                        docker ps -a \
                            --filter "name=${CONTAINER_NAME}"

                        docker logs ${CONTAINER_NAME} || true

                        exit 1
                    fi

                    echo "Docker API mapped to host port: $DOCKER_PORT"

                    echo "$DOCKER_PORT" > docker_api_port.txt

                    echo ""
                    echo "Waiting for Docker API..."

                    API_READY=false

                    for i in $(seq 1 20); do

                        if curl -fsS \
                            http://127.0.0.1:${DOCKER_PORT}/health \
                            > /dev/null 2>&1; then

                            echo "Docker API started successfully!"

                            API_READY=true
                            break
                        fi

                        echo "Waiting for Docker API... ($i/20)"
                        sleep 2
                    done

                    if [ "$API_READY" != "true" ]; then

                        echo "ERROR: Docker API failed to start."

                        echo ""
                        echo "========== CONTAINER STATUS =========="

                        docker ps -a \
                            --filter "name=${CONTAINER_NAME}"

                        echo ""
                        echo "========== CONTAINER LOGS =========="

                        docker logs ${CONTAINER_NAME} || true

                        echo ""
                        echo "========== DOCKER INSPECT =========="

                        docker inspect ${CONTAINER_NAME} \
                            --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}} Error={{.State.Error}}'

                        exit 1
                    fi

                    echo ""
                    echo "Docker API health response:"

                    curl -fsS \
                        http://127.0.0.1:${DOCKER_PORT}/health

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

                    if [ ! -f docker_api_port.txt ]; then
                        echo "ERROR: docker_api_port.txt not found."
                        exit 1
                    fi

                    DOCKER_PORT=$(cat docker_api_port.txt)

                    echo "Using Docker API port: $DOCKER_PORT"

                    echo ""
                    echo "-----------------------------------------"
                    echo "Test 1: Health Endpoint"
                    echo "-----------------------------------------"

                    curl -fsS \
                        http://127.0.0.1:${DOCKER_PORT}/health

                    echo ""
                    echo "Health test passed."

                    echo ""
                    echo "-----------------------------------------"
                    echo "Test 2: Prediction Endpoint"
                    echo "-----------------------------------------"

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
                        http://127.0.0.1:${DOCKER_PORT}/predict

                    echo ""
                    echo ""
                    echo "========================================="
                    echo "Docker API tests passed!"
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

                docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

                rm -f docker_api_port.txt

                echo "Cleanup completed."
            '''
        }

        success {
            echo "========================================="
            echo "CI/CD PIPELINE SUCCESS!"
            echo "========================================="
        }

        failure {
            echo "========================================="
            echo "CI/CD PIPELINE FAILED!"
            echo "========================================="

            sh '''
                echo ""
                echo "========== LOCAL API LOG =========="

                if [ -f api.log ]; then
                    cat api.log
                else
                    echo "No api.log found."
                fi

                echo ""
                echo "========== DOCKER CONTAINER =========="

                docker ps -a \
                    --filter "name=${CONTAINER_NAME}" || true
            '''
        }
    }
}