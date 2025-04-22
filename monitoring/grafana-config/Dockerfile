FROM grafana/grafana:11.5.2

USER root

COPY etc/grafana /etc/grafana
COPY var/grafana /var/lib/grafana
RUN chown -R 472:0 /etc/grafana /var/lib/grafana && \
    chmod -R 755 /etc/grafana /var/lib/grafana

USER 472

EXPOSE 3333
ENV GF_SERVER_HTTP_PORT=3333
CMD ["/run.sh"]