# Toodo Deploy Challenge

This minikube deployment was based on minikube running on an Ubuntu box running Ubuntu 20.04.

## Versions

1. minikube v1.9.2 with kubernetes 1.18
2. postgresql 11.7.0
3. gobuffalo/toodo app forked [here](https://github.com/charandas/toodo/tree/go-mod) for Dockerfile changes for go.mod

## Notes

1. kustomize with sops support, see [plugin](https://github.com/viaduct-ai/kustomize-sops). PGP key used is the demo key mentioned [here](https://github.com/viaduct-ai/kustomize-sops#6-configure-sops-via-sopsyaml)

	`kustomize build --enable_alpha_plugins deploy/base/ | kubectl apply -f-`
2. minikube addons: ingress, registry, and a local volume on minikube host for postgres pv
3. mozilla's [sops](https://github.com/mozilla/sops/releases)

## Networking

1. While the ingress is working, its only available locally on my linux box. To keep my leisure of working from my macbook on the go, I added a nodePort service, and used SOCAT to port-forward it on the host ip.
2. minikube registry was as simple as a port-forward, and didn't require multiple hops as it would with Docker for Mac.


## Future Improvements

1. The migrations and db creation runs as an init container in the toodo deployment. This unnecessarily slows down the scale up of the deployment. Factored out into its own k8s job, the scale up would become unimpeded, as the migrations don't need to be attempted per pod in the replicaset.
2. I could not find a way to make the CSRF token / Cookie session worked with locust. It would silently fail in gobuffalo, returning 302s for POST /items, and no errors in logs. When I inspected pgsql, no new items were created. I temporarily mitigated this by grabbing a token and cookie from my browser session.
3. Due to the session hack, I also did not attempt registering new users from within locust, and hence my tests use a single user for stress test.
4. The PG deployment can be updated for more shared_buffers and max_connections as needed, but some research showed me that an application that is well written would not need a large pool.
