FROM caddy:latest

COPY ./Caddyfile /etc/caddy/Caddyfile

EXPOSE 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]