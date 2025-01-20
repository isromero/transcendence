FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install -g live-server && npm install --include=dev
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
