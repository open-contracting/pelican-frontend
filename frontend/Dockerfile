FROM node:14 as build-stage
WORKDIR /workdir
COPY package*.json ./
# https://cli.vuejs.org/guide/deployment.html#docker-nginx
RUN npm install
COPY . .
RUN npm run build

FROM nginxinc/nginx-unprivileged:latest as production-stage
USER root
COPY --chown=nginx:root --from=build-stage /workdir/dist /usr/share/nginx/html
COPY --chown=nginx:root default.conf /etc/nginx/conf.d/default.conf
USER nginx
