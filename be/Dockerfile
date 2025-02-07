FROM python:3.13.1-slim
# RUN useradd -m imnotroot
WORKDIR /app
RUN apt update && apt install -y \
	postgresql-client \	
	&& apt clean

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# COPY --chown=iamnotroot:notroot. /app/
COPY . /app/
# USER iamnotroot
# Avoid buffering stdout and stderr (immediately print to console)
ENV PYTHONUNBUFFERED 1
# Avoid writing .pyc files (__pycache__) in local
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
#RUN /app/script_bbdd hay que añadir al CMD este script
RUN chmod +x /app/script_bbdd
CMD ["sh" , "/app/script_bbdd"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]