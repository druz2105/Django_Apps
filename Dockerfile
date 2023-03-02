ENV DEBIAN_FRONTEND=noninteractive
RUN wget -O - http://nginx.org/keys/nginx_signing.key | apt-key add - && \
echo "deb http://nginx.org/packages/debian/ buster nginx" | tee -a /etc/apt/sources.list && \
echo "deb-src http://nginx.org/packages/debian/ buster nginx" | tee -a /etc/apt/sources.list && \
apt-get update -y && \
apt-get install -y nginx supervisor && \
apt-get install -y nginx-extras && \
echo "daemon off;" >> /etc/nginx/nginx.conf && \
mkdir -p /var/log/voyage_control/ && \
rm -rf /var/lib/apt/lists/*