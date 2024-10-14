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

## 3. Activate the Virtual Environment

**On Windows:**

  ```bash
  myenv\Scripts\activate
  ```

## 4. Installing requirments.txt

**On Windows:**

  ```bash
  pip install -r requirments.txt
  ```

## 5. Navigate to the `manage.py` File

Change your directory to the location of the `manage.py` file:

```bash
cd path/to/your/project/
```

---

## 6. Run the Development Server

Start the Django development server by running:

```bash
python manage.py runserver 8000
```

The server will start at `http://127.0.0.1:8000/`.

---

## 7. Run the Consume Event

Run consume_event in a serperate terminal within the 'myenv' environment::


```bash
python manage.py consume_events
```

## 8. Run the Celery Worker

Run celery worker in a serperate terminal within the 'myenv' environment:

**On Windows:**
```bash
celery -A notification_service_api worker --loglevel=info -P eventlet
```
**On Linux:** [Untested]
```bash
celery -A notification_service_api worker --loglevel=info
```

