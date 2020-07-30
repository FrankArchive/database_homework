FROM node:alpine as builder

COPY ./homework_Vue /opt/build
WORKDIR /opt/build
RUN npm i
RUN npm run build

FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /opt/build/dist /var/www/html
