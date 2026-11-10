FROM node:22-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
USER 1001
EXPOSE 3030
CMD ["node","app.js"]
