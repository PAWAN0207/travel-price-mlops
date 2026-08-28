# End-to-End Travel Price Prediction MLOps Platform

An end-to-end Machine Learning and MLOps capstone project demonstrating the complete lifecycle of a travel flight price prediction system — from model development and validation to REST API deployment, Docker containerization, Kubernetes orchestration, Apache Airflow workflow automation, MLflow experiment tracking, Jenkins CI/CD, and Streamlit-based user interaction.

The primary production workflow focuses on **Flight Price Prediction using Regression**.

---

## 1. Project Overview

The travel and tourism industry generates large amounts of data related to flights, hotels, users, routes, agencies, and travel behavior.

This project uses travel-related datasets to build machine learning solutions and demonstrate how a trained model can be transformed into a production-oriented MLOps system.

The main objective is to predict flight prices based on travel-related features such as:

- Departure location
- Destination
- Flight type
- Flight duration
- Distance
- Travel agency
- Date-related information

The trained regression model is exposed through a Flask REST API, containerized using Docker, and deployed using Kubernetes.

Apache Airflow is used for workflow orchestration and model validation/evaluation, while MLflow is used for experiment tracking and model artifact management.

Jenkins automates testing and Docker-based CI/CD validation.

A Streamlit application provides a user-friendly interface for making flight price predictions.

---

## 2. Project Objectives

1. Build a machine learning regression model for flight price prediction.
2. Validate and evaluate the trained model.
3. Develop a REST API using Flask.
4. Containerize the API using Docker.
5. Deploy and scale the API using Kubernetes.
6. Automate model validation and evaluation using Apache Airflow.
7. Track experiments and model artifacts using MLflow.
8. Implement CI/CD using Jenkins.
9. Build an interactive Streamlit prediction application.
10. Demonstrate an end-to-end MLOps workflow.

---

## 3. Datasets

The project contains three main datasets:

### Flights Dataset

`data/flights.csv`

Contains flight-related information used for travel price prediction and analysis.

### Hotels Dataset

`data/hotels.csv`

Contains hotel-related travel information.

### Users Dataset

`data/users.csv`

Contains user-related travel information.

The primary production workflow demonstrated in this project uses the flight dataset.

---

## 4. Machine Learning Workflow

```text
Raw Travel Data
       |
       v
Data Exploration
       |
       v
Data Preprocessing
       |
       v
Feature Engineering
       |
       v
Model Development
       |
       v
Model Evaluation
       |
       v
Model Serialization
       |
       v
REST API
       |
       v
Docker
       |
       v
Kubernetes
```

The trained flight price prediction model is stored as:

```text
models/flight_price_model.pkl
```

The Flask API loads this serialized model during application startup.

---

## 5. Flight Price Regression Model

The main production model is a regression model designed to predict flight prices.

Example input features include:

```text
from
to
flightType
time
distance
agency
year
month
day
day_of_week
```

Example request:

```json
{
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
}
```

Example response:

```json
{
    "predicted_price": 1434.38,
    "status": "success"
}
```

---

## 6. Flask REST API

The machine learning model is exposed through a Flask REST API.

Application:

```text
api/app.py
```

### Health Endpoint

```text
GET /health
```

Example response:

```json
{
    "model_loaded": true,
    "status": "healthy"
}
```

### Prediction Endpoint

```text
POST /predict
```

The endpoint accepts flight details in JSON format and returns the predicted flight price.

---

## 7. API Testing

Automated API tests are located in:

```text
tests/test_api.py
```

The tests verify:

- Home endpoint
- Health endpoint
- Prediction endpoint

Run:

```bash
pytest -v tests/test_api.py
```

Verified CI result:

```text
test_home       PASSED
test_health     PASSED
test_predict    PASSED

3 passed
```

---

## 8. Docker

The Flask API is containerized using Docker.

Docker configuration:

```text
Dockerfile
```

Build:

```bash
docker build -t travel-price-api .
```

Run:

```bash
docker run -d --name travel-price-api -p 5000:5000 travel-price-api
```

Check:

```bash
curl.exe http://127.0.0.1:5000/health
```

Expected:

```json
{
    "model_loaded": true,
    "status": "healthy"
}
```

---

## 9. Docker API Validation

The Dockerized API is tested from inside the container.

The CI pipeline validates:

- Container startup
- Health endpoint
- Prediction endpoint
- HTTP 200 response
- Successful prediction response

Example:

```json
{
    "predicted_price": 1434.38,
    "status": "success"
}
```

---

## 10. Kubernetes

Kubernetes is used to deploy and scale the Flask API.

Configuration:

```text
kubernetes/
├── deployment.yaml
└── service.yaml
```

The deployment was verified with two running API replicas:

```text
travel-price-api-6847cd9cb8-9r5ff   1/1   Running
travel-price-api-6847cd9cb8-9vdxh   1/1   Running
```

### Kubernetes Service

Service:

```text
travel-price-api-service
```

Configuration:

```text
Type: NodePort
Port: 5000
TargetPort: 5000
NodePort: 32659
```

The service routes traffic to the running API pods.

### Kubernetes Internal Connectivity Test

The service was successfully tested from inside the Kubernetes cluster:

```bash
kubectl run test-curl --rm -i   --restart=Never   --image=curlimages/curl   -- curl -v http://travel-price-api-service:5000/health
```

Verified response:

```text
HTTP/1.1 200 OK
```

```json
{
    "model_loaded": true,
    "status": "healthy"
}
```

---

## 11. Apache Airflow

Apache Airflow is used for workflow orchestration.

Important files:

```text
airflow-compose.yml
airflow.Dockerfile

airflow/
└── dags/
    └── travel_price_pipeline.py
```

Main DAG:

```text
travel_price_pipeline
```

Workflow:

```text
Model Validation
       |
       v
Model Evaluation
       |
       v
MLflow Tracking
```

### Model Validation

The validation task loads:

```text
models/flight_price_model.pkl
```

and verifies that the trained model can be successfully loaded.

### Model Evaluation

The evaluation task:

1. Loads the trained model.
2. Creates sample input.
3. Generates a prediction.
4. Connects to MLflow.
5. Creates or uses the configured MLflow experiment.
6. Logs parameters.
7. Logs the prediction metric.
8. Stores the model artifact.

MLflow tracking URI inside Airflow:

```text
http://mlflow:5000
```

Experiment:

```text
travel-price-prediction
```

---

## 12. MLflow

MLflow is used for experiment tracking and model artifact management.

MLflow-related files:

```text
mlflow/
└── log_existing_model.py
```

Tracking artifacts are maintained under:

```text
mlruns/
```

The evaluation workflow logs information including:

- Model type
- Flight type
- Agency
- Source
- Destination
- Flight time
- Distance
- Year
- Month
- Day
- Day of week
- Predicted price

The model artifact is stored as:

```text
artifacts/
└── model/
    └── flight_price_model.pkl
```

A successful MLflow run was created during project validation.

---

## 13. Jenkins CI/CD

Jenkins is used to automate continuous integration and Docker validation.

Pipeline configuration:

```text
Jenkinsfile
```

Workflow:

```text
Checkout Code
      |
      v
Setup Python Environment
      |
      v
Install Dependencies
      |
      v
Start Local Flask API
      |
      v
Run API Tests
      |
      v
Stop Local API
      |
      v
Build Docker Image
      |
      v
Run Docker Container
      |
      v
Docker Health Test
      |
      v
Docker Prediction Test
      |
      v
Cleanup
```

---

## 14. Jenkins Pipeline Verification

The Jenkins pipeline was successfully executed.

### API Tests

```text
3 passed
```

### Docker Build

```text
Docker image built successfully.
```

### Docker Health Test

```text
Health test passed.
```

### Docker Prediction Test

```text
Prediction test passed.
```

### Final Status

```text
CI/CD PIPELINE SUCCESS!
Finished: SUCCESS
```

This demonstrates automated validation of the Flask API and Dockerized ML application.

---

## 15. Streamlit Application

A Streamlit application provides a user-friendly interface for the flight price prediction system.

Application:

```text
streamlit/app.py
```

The interface accepts:

- From
- To
- Flight Type
- Flight Time
- Distance
- Agency

The application sends the input to:

```text
POST /predict
```

and displays the predicted price.

Run:

```bash
streamlit run streamlit/app.py
```

---

## 16. Streamlit API Configuration

The application supports:

```text
API_URL
```

Default:

```text
http://localhost:5000
```

This allows the Streamlit application to communicate with different API environments without changing the application code.

---

## 17. End-to-End MLOps Architecture

```text
                  +----------------------+
                  |   Travel Datasets    |
                  | Users / Flights /    |
                  | Hotels               |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  | Machine Learning     |
                  | Flight Price         |
                  | Regression Model     |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  | Serialized Model     |
                  | flight_price_model   |
                  | .pkl                 |
                  +----------+-----------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
     +-----------------+           +-----------------+
     | Apache Airflow  |           |     MLflow      |
     | Validation &    |---------->| Experiment &    |
     | Evaluation      |           | Artifact Track. |
     +--------+--------+           +-----------------+
              |
              v
     +---------------------+
     |     Flask API       |
     | /health             |
     | /predict            |
     +----------+----------+
                |
                v
       +-----------------+
       |      Docker     |
       | Containerized   |
       | API             |
       +--------+--------+
                |
                v
       +-----------------+
       |   Kubernetes    |
       | Multiple API    |
       | Replicas        |
       +--------+--------+
                |
          +-----+-----+
          |           |
          v           v
   +------------+ +------------+
   | Streamlit  | | API Client |
   | Web App    | |            |
   +------------+ +------------+

             Jenkins CI/CD
                   |
                   v
          Automated Testing
                   |
                   v
             Docker Build
                   |
                   v
          Container Testing
```

---

## 18. Complete MLOps Workflow

```text
Data
 |
 v
Model Development
 |
 v
Model Validation
 |
 v
Model Evaluation
 |
 v
MLflow Tracking
 |
 v
Flask REST API
 |
 v
API Testing
 |
 v
Docker Build
 |
 v
Docker Testing
 |
 v
Kubernetes Deployment
 |
 v
Kubernetes Scaling
 |
 v
Streamlit Application
```

Jenkins provides automated CI/CD validation.

Apache Airflow provides workflow orchestration.

MLflow provides experiment and artifact tracking.

Kubernetes provides container orchestration and scaling.

---

## 19. Project Structure

```text
travel-capstone/
|
├── api/
│   └── app.py
|
├── airflow/
│   ├── dags/
│   │   └── travel_price_pipeline.py
│   ├── logs/
│   └── plugins/
|
├── data/
│   ├── flights.csv
│   ├── hotels.csv
│   └── users.csv
|
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
|
├── mlflow/
│   └── log_existing_model.py
|
├── mlruns/
│   └── MLflow tracking artifacts
|
├── models/
│   └── flight_price_model.pkl
|
├── notebooks/
|
├── streamlit/
│   └── app.py
|
├── src/
|
├── tests/
│   └── test_api.py
|
├── Dockerfile
├── Jenkinsfile
├── airflow-compose.yml
├── airflow.Dockerfile
├── jenkins.Dockerfile
├── requirements.txt
├── airflow-requirements.txt
├── .gitignore
└── README.md
```

---

## 20. Local Setup

### Clone Repository

```bash
git clone https://github.com/PAWAN0207/travel-price-mlops.git
cd travel-price-mlops
```

### Create Python Environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scriptsctivate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 21. Run Flask API

```bash
python api/app.py
```

Check:

```bash
curl.exe http://127.0.0.1:5000/health
```

Expected:

```json
{
    "model_loaded": true,
    "status": "healthy"
}
```

---

## 22. Run API Tests

```bash
pytest -v tests/test_api.py
```

Expected:

```text
3 passed
```

---

## 23. Run Docker

```bash
docker build -t travel-price-api .
```

```bash
docker run -d   --name travel-price-api   -p 5000:5000   travel-price-api
```

Check:

```bash
curl.exe http://127.0.0.1:5000/health
```

---

## 24. Run Kubernetes

```bash
kubectl apply -f kubernetes/deployment.yaml
```

```bash
kubectl apply -f kubernetes/service.yaml
```

Check:

```bash
kubectl get pods
```

```bash
kubectl get services
```

```bash
kubectl get deployment
```

---

## 25. Run Apache Airflow

Start:

```bash
docker compose -f airflow-compose.yml up -d
```

Check:

```bash
docker compose -f airflow-compose.yml ps
```

Trigger DAG:

```bash
docker exec travel-airflow-scheduler airflow dags trigger travel_price_pipeline
```

Check runs:

```bash
docker exec travel-airflow-scheduler airflow dags list-runs -d travel_price_pipeline -o table
```

---

## 26. Run MLflow

```bash
python mlflow/log_existing_model.py
```

This creates an MLflow tracking run and stores the model artifact.

---

## 27. Run Streamlit

```bash
streamlit run streamlit/app.py
```

The Streamlit application communicates with the Flask API using:

```text
API_URL
```

---

## 28. Monitoring and Troubleshooting

### API Health

```bash
curl.exe http://127.0.0.1:5000/health
```

The endpoint verifies API availability and model loading status.

### Airflow

Airflow provides visibility into:

- DAG runs
- Task execution
- Task failures
- Task logs
- Model validation
- Model evaluation

### MLflow

MLflow provides visibility into:

- Experiment runs
- Parameters
- Prediction metrics
- Model artifacts

### Kubernetes

```bash
kubectl get pods
kubectl get services
kubectl get deployments
kubectl describe service travel-price-api-service
```

### Jenkins

Jenkins provides:

- Build status
- Test results
- Docker build results
- API validation
- Pipeline logs
- Cleanup status

---

## 29. Troubleshooting

### Flask API Not Reachable

```bash
curl.exe http://127.0.0.1:5000/health
```

### Docker Container Problem

```bash
docker ps
docker logs travel-price-api
```

### Kubernetes Pod Problem

```bash
kubectl get pods
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Kubernetes Service Problem

```bash
kubectl describe service travel-price-api-service
```

Test from inside the cluster:

```bash
kubectl run test-curl   --rm -i   --restart=Never   --image=curlimages/curl   -- curl http://travel-price-api-service:5000/health
```

---

## 30. CI/CD Quality Gates

The Jenkins pipeline validates:

```text
✓ Source code checkout
✓ Python environment
✓ Dependency installation
✓ Flask API startup
✓ API health
✓ API tests
✓ Docker image build
✓ Docker container startup
✓ Docker health endpoint
✓ Docker prediction endpoint
✓ Container cleanup
```

The latest verified Jenkins pipeline completed successfully.

---

## 31. Future Improvements

Possible future improvements include:

- Automated model retraining
- Model version promotion
- Automated model performance thresholds
- Data drift detection
- Model drift monitoring
- Automated model registry workflow
- Cloud deployment
- Kubernetes Ingress
- Horizontal Pod Autoscaling
- Prometheus/Grafana monitoring
- Automated deployment after successful CI
- Secure secrets management
- Authentication and authorization
- Automated rollback mechanisms

---

## 32. Technologies Used

| Area | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| API | Flask |
| API Testing | Pytest |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Workflow Automation | Apache Airflow |
| Experiment Tracking | MLflow |
| CI/CD | Jenkins |
| User Interface | Streamlit |
| Version Control | Git / GitHub |

---

## 33. Key MLOps Concepts Demonstrated

```text
Machine Learning
       +
REST API
       +
Docker
       +
Kubernetes
       +
Apache Airflow
       +
MLflow
       +
Jenkins CI/CD
       +
Streamlit
       =
End-to-End MLOps System
```

The project demonstrates how a machine learning model can be validated, tracked, packaged, deployed, orchestrated, tested, and served to users through an integrated MLOps workflow.

---

## 34. Author

**Pawan Prasad**

Data Analytics | Machine Learning | MLOps

GitHub:  
https://github.com/PAWAN0207

Project Repository:  
https://github.com/PAWAN0207/travel-price-mlops

---

## 35. Project Highlights

- End-to-end flight price prediction system
- Flask REST API
- Dockerized ML application
- Kubernetes deployment with multiple replicas
- Apache Airflow workflow orchestration
- MLflow experiment tracking
- Jenkins CI/CD pipeline
- Automated API testing
- Docker health and prediction testing
- Streamlit user interface
- Git/GitHub version control

---

## License

This project was developed as part of an academic MLOps capstone project.
