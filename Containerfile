FROM default-route-openshift-image-registry.apps.semace.6z71.p2.openshiftapps.com/openshift/nginx:latest

COPY --chown=default nginx.conf /etc/nginx/
COPY --chown=default 404.html /data/site/
COPY --chown=default mkdocs /data/

EXPOSE 8089

USER 1001 

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
