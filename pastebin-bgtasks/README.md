# pastebin-bgtasks

runs background tasks for pastebin-app [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/pastebin-clone).

docker instructions:

```bash
# build the image
docker build -t pastebin-bgtasks .

# run the image
docker run -p 80:80 -p 443:443 --name pastebin-bgtasks --restart always -d pastebin-bgtasks

# push to docker hub
docker tag pastebin-bgtasks nathanesau/pastebin-clone:pastebin-bgtasks
docker push nathanesau/pastebin-clone:pastebin-bgtasks
```
