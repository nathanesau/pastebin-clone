# pastebin-app

start up flask app using port 5001 dockerhub link](https://hub.docker.com/repository/docker/nathanesau/pastebin-clone)

```bash
# build the image
docker build -t pastebin-app .

# run the image
docker run -p 5001:5001 --name pastebin-app -d pastebin-app

# push to docker hub
docker tag pastebin-app nathanesau/pastebin-clone:pastebin-app
docker push nathanesau/pastebin-clone:pastebin-app
```
