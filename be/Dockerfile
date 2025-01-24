FROM python:3.13.1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
RUN chmod 755 /app/script_bbdd
# Avoid buffering stdout and stderr (immediately print to console)
ENV PYTHONUNBUFFERED 1
# Avoid writing .pyc files (__pycache__) in local
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
#RUN /app/script_bbdd hay que añadir al CMD este script
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]