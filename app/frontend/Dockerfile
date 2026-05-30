# Stage 1: Build the React app

FROM node:20-alpine AS build

WORKDIR /app

RUN npm install -g npm@latest

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Stage 2: Serve the app with Nginx

FROM nginx:stable-alpine

ARG FRONTEND_INTERNAL_PORT=81
ENV FRONTEND_INTERNAL_PORT=${FRONTEND_INTERNAL_PORT}

RUN echo "server { \
    listen ${FRONTEND_INTERNAL_PORT}; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    try_files \$uri \$uri/ /index.html; \
    } \
    location /api/ { \
    proxy_pass http://echocad_server:8000/; \
    proxy_set_header Host \$host; \
    proxy_set_header X-Real-IP \$remote_addr; \
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \
    proxy_set_header X-Forwarded-Proto \$scheme; \
    } \
    }" > /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE ${FRONTEND_INTERNAL_PORT}

CMD ["nginx", "-g", "daemon off;"]