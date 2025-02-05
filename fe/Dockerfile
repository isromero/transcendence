FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install -g live-server && \
	npm install --include=dev
	# && npm install prom-client express
COPY . .
EXPOSE 3001
CMD ["sh", "-c", "node metrics.js & npm start"]
