# FROM node:18-alpine AS builder
# WORKDIR /app


# COPY . .



# RUN npm install
# RUN npm run build

# # ---------- Serve stage ----------
# FROM nginx:alpine
# COPY --from=builder /app/build /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
# Build stage
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
