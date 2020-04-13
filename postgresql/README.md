# postgres manifests for kustomize

We use bitnami's postgres chart to generate the plain manifest.

```
helm --release-name toodo template  bitnami/postgresql -f ./values.yml > ../deploy/base/db.yml
```
