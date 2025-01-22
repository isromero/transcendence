FROM python:3.13.1-alpine3.21
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
# Avoid buffering stdout and stderr (immediately print to console)
ENV PYTHONUNBUFFERED 1
# Avoid writing .pyc files (__pycache__) in local
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]