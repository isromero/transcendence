FROM prom/prometheus:latest

USER root
RUN addgroup  prometheus && \
    adduser -G prometheus -D prometheus
RUN chown -R prometheus:prometheus /etc/prometheus /prometheus
USER prometheus
COPY prometheus.yml /etc/prometheus/prometheus.yml
EXPOSE 9090


# FROM prom/prometheus:latest

# COPY prometheus.yml /etc/prometheus/prometheus.yml

# EXPOSE 9090

# RUN useradd -m prometheus

# FROM prom/prometheus

# RUN addgroup -g 65532 prometheus && \
#     adduser -u 65532 -G prometheus -D prometheus

# COPY --chown=prometheus:prometheus prometheus.yml /etc/prometheus/prometheus.yml

# RUN chown -R prometheus:prometheus /etc/prometheus /prometheus

# USER prometheus

# EXPOSE 9090

# CMD [ "/bin/prometheus", "--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus" ]
