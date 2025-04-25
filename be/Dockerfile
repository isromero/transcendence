FROM python:3.13.1-slim

WORKDIR /app
RUN apt update && apt install -y \
	postgresql-client \	
	&& apt clean

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
RUN mkdir -p /app/apps/core/migrations && \
	touch /app/apps/core/migrations/__init__.py

# Avoid buffering stdout and stderr (immediately print to console)
ENV PYTHONUNBUFFERED 1

# Avoid writing .pyc files (__pycache__) in local
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000

CMD ["sh" , "/app/script_bbdd"]
