#!/bin/sh

WEB_READY=/home/nginx/web_ready

if ! /usr/bin/test -f "$WEB_READY"; then

    # substitute the env variables
    export DOLLAR='$'
    /bin/grep -v "^\s*\#" /tmp/nginx.conf.template > /tmp/nginx.conf.template.nocomments
    /usr/local/bin/envsubst < /tmp/nginx.conf.template.nocomments > /etc/nginx/conf.d/nginx.conf

    # clean
    /bin/rm /etc/nginx/conf.d/default.conf
    /bin/rm /tmp/nginx.conf.template
    /bin/rm /tmp/nginx.conf.template.nocomments

    # set a flag that the web server configuration is ready
    /bin/touch $WEB_READY
fi

# run
/usr/sbin/nginx -g "daemon off;"