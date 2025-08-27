FROM registry.access.redhat.com/ubi9/python-312

USER 0

ENV MKDOCS=/opt/app-root/mkdocs

RUN rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    dnf install -y inotify-tools && \
    dnf install -y pango nginx && \
    pip install --upgrade pip && \
    pip install mkdocs mkdocs-macros-plugin mkdocs-with-pdf weasyprint  mkdocs-minify-plugin mkdocs-mermaid2-plugin mkdocs-static-i18n[material] mkdocs-static-i18n easydict==1.2 psycopg2 mkdocs-section-index mkdocs-literate-nav pyyaml jq yq && \
    mkdir -p $MKDOCS/site && \
    echo "true" > $MKDOCS/site/ready.json && \
    chown -R default $MKDOCS /var/log/nginx /usr/share/nginx /etc/nginx 

COPY --chown=default nginx.conf /etc/nginx/
COPY --chown=default 404.html $MKDOCS/site/
COPY --chown=default mkdocs $MKDOCS/

EXPOSE 8089

ENV PATH=/opt/app-root/bin:$PATH

USER default 

WORKDIR /opt/app-root/mkdocs

ENTRYPOINT nginx -g "daemon off;"


