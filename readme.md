# Airflow-Django Project

This project integrates **Apache Airflow** and **Django** to simulate KPI calculations using an Airflow DAG and a Django-based API backend.

## Project Structure

```
project/
├── dags/                   # Airflow DAGs directory
├── simulator_project/      # Django project folder
├── simulators/             # Django app for simulators
├── db.sqlite3              # Django SQLite database
├── dockerfile              # Docker configuration file
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
```

---

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- WSL (if running Airflow on Windows)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Django

#### A. Run Migrations

```bash
python manage.py migrate
```

#### B. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

#### C. Update `ALLOWED_HOSTS`
In `simulator_project/settings.py`, update the `ALLOWED_HOSTS`:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '<your-ip>']
```

---

### 5. Run Django Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access the server at `http://localhost:8000`.

---

### 6. Configure and Run Airflow

#### A. Initialize Airflow

Ensure the Airflow environment is initialized:

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
```

#### B. Create an Airflow User

```bash
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

#### C. Start Airflow Scheduler and Webserver

```bash
airflow scheduler &
airflow webserver -p 8080 &
```

Access Airflow at `http://localhost:8080`.

#### D. Verify DAGs
Ensure the DAGs are placed in the `dags/` directory. They will appear in the Airflow UI.

---

## Using the Application

### 1. Django API
- The KPI calculation endpoint is available at:
  ```
  POST /api/calculate-kpi/
  ```
  Example payload:
  ```json
  {
      "value": 100,
      "kpi_id": 1
  }
  ```

- Test the API using Postman or `curl`:
  ```bash
  curl -X POST http://localhost:8000/api/calculate-kpi/ \
       -H "Content-Type: application/json" \
       -d '{"value": 100, "kpi_id": 1}'
  ```

### 2. Airflow DAG
- Trigger the `kpi_simulator` DAG from the Airflow UI.
- The DAG fetches KPIs and sends requests to the Django API.

---

## Docker (Optional)

### 1. Build the Docker Image

```bash
docker build -t airflow-django .
```

### 2. Run the Docker Container

```bash
docker run -p 8000:8000 -p 8080:8080 airflow-django
```

---

## Troubleshooting

### Common Issues

1. **Connection Refused Between Airflow and Django**
   - Ensure both services are running.
   - Use `0.0.0.0` as the Django host and the correct IP for Airflow to connect.

2. **Missing Dependencies**
   - Ensure all packages in `requirements.txt` are installed.

---

## License

This project is licensed under the MIT License.

