# FROM caddy:latest

# # COPY ./media /app/media

# EXPOSE 443

# COPY ./Caddyfile /etc/caddy/Caddyfile

# CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]


FROM caddy:latest

# RUN addgroup --system caddygroup && adduser --system --ingroup caddygroup caddyuser
# RUN mkdir -p /app/media && chown -R caddyuser:caddygroup /app/media

COPY ./Caddyfile /etc/caddy/Caddyfile

# RUN chown -R caddyuser:caddygroup /etc/caddy /data /config /app

# USER caddyuser

EXPOSE 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]