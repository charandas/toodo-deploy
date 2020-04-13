# stats (from Locust)

There are 2 pairs of files here. I captured the `top` stats as the test was running from within minikube vm.

The other `requests_` file is from locust when the test was run with 1k users but building at 100/sec, vs run with 4k users, but building at 1000/sec.
As one may see, the `requests_` CSVs don't have any failures. For both tests, I ran with 5 replicas of the `toodo` deployment.

For the locust run, only `POST` `/items` was attempted with a task weight of 1 (`@task(1)`), as can be seen the locustfile.
