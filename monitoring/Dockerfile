FROM prom/prometheus:latest

USER root
RUN addgroup  prometheus && \
    adduser -G prometheus -D prometheus
RUN chown -R prometheus:prometheus /etc/prometheus /prometheus
USER prometheus
COPY prometheus.yml /etc/prometheus/prometheus.yml
EXPOSE 9090

