# Setup Instructions

Follow these steps to set up and run the Django project:

## 1. Install Python 3.10 (if not installed)

Download and install Python 3.10 from the [official Python website](https://www.python.org/downloads/release/python-3100/).

---

## 2. Create a Virtual Environment

Open your terminal or command prompt and run:

```bash
python -m venv myenv
```

This command creates a virtual environment named `myenv`.

---
## 3. Run one instance of RabbiteMQ server if not already running.

**On Windows: Run as admin**

  ```bash
  rabbitmq-server.bat
  ```


## 4. Activate the Virtual Environment

**On Windows:**

  ```bash
  myenv\Scripts\activate
  ```

## 5. Installing requirments.txt

**On Windows:**

  ```bash
  pip install -r requirments.txt
  ```

## 6. Navigate to the `manage.py` File

Change your directory to the location of the `manage.py` file:

```bash
cd path/to/your/project/
```

---

## 7. Run the Development Server

Start the Django development server by running:

```bash
python manage.py runserver 7000
```

The server will start at `http://127.0.0.1:7000/`.

---

## 8. Run the Consume Event

Run consume_event in a serperate terminal within the 'myenv' environment::


```bash
python manage.py consume_events
```

## 9. Run the Celery Worker

Run celery worker with node name as 'scheduled_worker' in a serperate terminal within the 'myenv' environment:

**On Windows:**
```bash
celery -A report_service_api worker --pool=gevent --loglevel=info --hostname=scheduled_worker
```
**On Linux:** [Untested]
```bash
celery -A report_service_api worker --loglevel=info --hostname=scheduled_worker
```

## 10. Run the Celery Beats

Run celery worker in a serperate terminal within the 'myenv' environment:
**On Windows:**
```bash
celery -A notification_service_api worker --loglevel=info -P eventlet
```
---

# API Endpoints

## 1. Report Generate
```link
http://127.0.0.1:7000/reports/generate/
```


## 2. Report History
```link
http://127.0.0.1:7000/reports/history/
```


## 3. Report Download
```link
http://127.0.0.1:7000/reports/<int:pk>/download/
```
