FROM registry.access.redhat.com/ubi9/python-312

USER 0

RUN dnf install -y pango nginx && \
    pip install --upgrade pip && \
    pip install mkdocs mkdocs-macros-plugin mkdocs-with-pdf weasyprint  mkdocs-minify-plugin mkdocs-mermaid2-plugin mkdocs-static-i18n[material] mkdocs-static-i18n easydict==1.2 psycopg2 mkdocs-section-index mkdocs-literate-nav pyyaml jq yq && \
    mkdir -p /data/site && \
    echo "true" > /data/site/ready.json && \
    chown -R default /data /var/log/nginx /usr/share/nginx /etc/nginx

COPY --chown=default nginx.conf /etc/nginx/
COPY --chown=default 404.html /data/site/
COPY --chown=default mkdocs /data/

EXPOSE 8089

ENV PATH=/opt/app-root/bin:$PATH

USER 1001 

WORKDIR /data

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
