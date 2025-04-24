FROM node:20-alpine
# RUN addgroup --system fe && \
#     adduser --system --ingroup fe --home /app fe 
WORKDIR /app
COPY package*.json ./
RUN npm install --include=dev
# RUN npm install -g live-server && \
# 	npm install --include=dev
COPY . .
# RUN chown -R fe:fe /app/public
# RUN chmod -R u=rwX,g=rX,o= /app/public
# USER fe
EXPOSE 3001
CMD ["sh", "-c", "node metrics.js & npm start"]
