FROM node:14 as build-stage
WORKDIR /workdir
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginxinc/nginx-unprivileged:latest as production-stage
USER root
COPY --from=build-stage --chown=nginx:nginx /workdir/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
USER nginx
