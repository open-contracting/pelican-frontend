# https://cli.vuejs.org/guide/deployment.html#docker-nginx
FROM node:18 as build-stage

WORKDIR /workdir

COPY package*.json ./
RUN npm install

COPY . .
ARG VUE_APP_API_BASE_URL
ENV VUE_APP_API_BASE_URL=${VUE_APP_API_BASE_URL:-http://127.0.0.1:8000/}
RUN VUE_APP_API_BASE_URL=${VUE_APP_API_BASE_URL} npx vue-cli-service build

FROM nginxinc/nginx-unprivileged:latest as production-stage
USER root
COPY --chown=nginx:root --from=build-stage /workdir/dist /usr/share/nginx/html
COPY --chown=nginx:root default.conf /etc/nginx/conf.d/default.conf
USER nginx
