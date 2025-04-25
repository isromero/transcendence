FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install --include=dev

COPY . .

EXPOSE 3001
CMD ["sh", "-c", "node metrics.js & npm start"]
