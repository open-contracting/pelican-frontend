# https://cli.vuejs.org/guide/deployment.html#docker-nginx
FROM node:16 as build-stage-vue

WORKDIR /workdir

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginxinc/nginx-unprivileged:latest as production-stage
USER root
COPY --chown=nginx:root --from=build-stage-vue /workdir/dist /usr/share/nginx/html
COPY --chown=nginx:root default.conf /etc/nginx/conf.d/default.conf
USER nginx
