FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install -g live-server && npm install --include=dev
COPY . .
EXPOSE 3001
CMD ["npm", "start"]
