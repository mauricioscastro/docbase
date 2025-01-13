FROM image-registry.openshift-image-registry.svc.cluster.local:5000/openshift/nginx:latest

COPY --chown=default nginx.conf /etc/nginx/
COPY --chown=default 404.html /data/site/
COPY --chown=default mkdocs /data/

EXPOSE 8089

USER 1001 

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
