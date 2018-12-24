FROM griffinplus/base-supervisor
MAINTAINER Sascha Falk <sascha@falk-online.eu>

# Update image and install additional packages
RUN apt-get -y update && \
  apt-get -y install \
    nginx \
    php7.2-bcmath \
    php7.2-bz2 \
    php7.2-curl \
    php7.2-dba \
    php7.2-enchant \
    php7.2-fpm \
    php7.2-gd \
    php7.2-gmp \
    php7.2-imap \
    php7.2-intl \
    php7.2-json \
    php7.2-ldap \
    php7.2-mbstring \
    php7.2-mysql \
    php7.2-odbc \
    php7.2-opcache \
    php7.2-pgsql \
    php7.2-pspell \
    php7.2-readline \
    php7.2-recode \
    php7.2-sqlite3 \
    php7.2-tidy \
    php7.2-xml \
    php7.2-xmlrpc \
    php7.2-xsl \
    php7.2-zip && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Copy prepared files into the image
COPY target /

# Remove superfluous files and adjust ownership and permissions
RUN \
  rm /var/www/html/index.nginx-debian.html && \
  chown -R www-data:www-data /var/www

# Expose port 80 (HTTP) only
# (SSL termination is done by a reverse proxy)
EXPOSE 80
