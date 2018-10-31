# Docker-Deploy
docker deploy data for hx


# Usage

It's very easy to use. Please run "./install.sh" to start the docker container.

# Troubleshot

Sometimes the "main_chain" container will be in wrong state. Please check ./hx/logs/* for details.
If the log files are not refreshed please restart "main_chain" container through the command:

```
docker stop main_chain
docker start main_chain
```
