FROM prom/prometheus:latest

USER root
RUN addgroup --system prometheus && \
    adduser --system --ingroup prometheus --uid 1000 prometheus
RUN chown -R prometheus:prometheus /etc/prometheus /prometheus
USER prometheus
COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY alert.rules.yml /etc/prometheus/alert.rules.yml
EXPOSE 9090
