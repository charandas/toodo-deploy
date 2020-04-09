# Toodo Deploy Challenge

Versions:

1. minikube v1.9.2 with kubernetes 1.18
2. postgresql 11.7.0
3. gobuffalo/toodo app forked [here](https://github.com/charandas/toodo/tree/go-mod) for Dockerfile changes for go.mod

Notes:

1. kustomize with sops support, see [plugin](https://github.com/viaduct-ai/kustomize-sops). PGP key used is the demo key mentioned [here](https://github.com/viaduct-ai/kustomize-sops#6-configure-sops-via-sopsyaml)

	`kustomize build --enable_alpha_plugins deploy/base/ | kubectl apply -f-`
2. bitnami's postgres chart, plain manifest generated using:

	`helm --release-name toodo template  bitnami/postgresql --set global.postgresql.existingSecret="postgres-secret" --set persistence.existingClaim=postgres-pvc`
3. minikube addons: ingress, registry, and a local volume on minikube host for postgres pv
4. mozilla's [sops](https://github.com/mozilla/sops/releases)
