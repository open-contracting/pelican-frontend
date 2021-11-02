# build stage
FROM node:14-alpine as build-stage
# https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md#node-gyp-alpine
WORKDIR /workdir
RUN  apk add --no-cache --virtual .gyp python2 make g++
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build -- --mode docker

# production stage
FROM nginxinc/nginx-unprivileged:latest as production-stage
USER root
COPY --from=build-stage --chown=nginx:nginx /workdir/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
USER nginx
