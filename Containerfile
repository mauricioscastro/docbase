FROM default-route-openshift-image-registry.apps.semace.6z71.p2.openshiftapps.com/openshift/nginx:latest

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
