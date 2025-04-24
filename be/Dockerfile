FROM python:3.13.1-slim
# RUN addgroup --system django && \
#     adduser --system --ingroup django --uid 1000 --home /app django 
WORKDIR /app
RUN apt update && apt install -y \
	postgresql-client \	
	&& apt clean

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
RUN mkdir -p /app/apps/core/migrations && \
	touch /app/apps/core/migrations/__init__.py
	# touch /app/apps/core/migrations/__init__.py && \
# 	chown -R django:django /app && \
# 	chmod -R u+w /app/apps/core/migrations

# USER django
# Avoid buffering stdout and stderr (immediately print to console)
ENV PYTHONUNBUFFERED 1
# Avoid writing .pyc files (__pycache__) in local
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
# RUN chmod +x /app/script_bbdd
# RUN echo ls -lh /app
CMD ["sh" , "/app/script_bbdd"]
# CMD ["uvicorn", "config.asgi:application", "--reload", "--host", "0.0.0.0", "--port", "8000"]
