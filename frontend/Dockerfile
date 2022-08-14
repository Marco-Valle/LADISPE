### FRONTEND BUILDER

# pull official base image
FROM node:16.16.0-alpine as frontend_builder

# set work directory
RUN mkdir -p /usr/src/

# copy the code
COPY . /usr/src/frontend
WORKDIR /usr/src/frontend

# compile
RUN npm install
RUN npm run build


### NGINX

# pull official base image
FROM nginx:1.22.0-alpine

# set the home
ENV NGINX_DIR=/home/nginx
RUN mkdir -p $NGINX_DIR
WORKDIR $NGINX_DIR

# copy the frontend code in www
COPY --from=frontend_builder /usr/src/frontend/dist /home/app/www

# set the correct permissions to www
RUN chown -R nginx:nginx /home/app/www

# create the directory for ssl
RUN mkdir -p /etc/ssl/ladispe

# copy the template
COPY ./nginx/nginx.conf.template /tmp/nginx.conf.template

# copy entrypoint
COPY ./nginx/entrypoint.sh .
RUN sed -i 's/\r$//g'  $NGINX_DIR/entrypoint.sh
RUN chmod +x  $NGINX_DIR/entrypoint.sh

# entrypoint
ENTRYPOINT ["/home/nginx/entrypoint.sh"]