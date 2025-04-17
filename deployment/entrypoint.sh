#!/bin/sh

chown -R caddyuser:caddygroup /app/media

chmod -R u+rwX /app/media

exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile