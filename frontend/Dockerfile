
FROM node:18-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Inject biến môi trường lúc build
COPY .env .env

RUN npm run build

# Serve static build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
