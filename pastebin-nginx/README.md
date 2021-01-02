# pastebin-nginx

to allow hosting multiple docker sites in same droplet, we should create multiple sites exposed on port 80 [dockerhub link](https://hub.docker.com/repository/docker/nathanesau/pastebin-clone).

docker instructions:

```bash
# build the image
docker build -t pastebin-nginx .

# run the image
docker run -p 80:80 -p 443:443 --name pastebin-nginx --restart always -d pastebin-nginx

# push to docker hub
docker tag pastebin-nginx nathanesau/pastebin-clone:pastebin-nginx
docker push nathanesau/pastebin-clone:pastebin-nginx
```

install nginx as service (for digital-ocean):

```bash
# install nginx
sudo apt-get install nginx

# start nginx
sudo systemctl enable nginx

# configuration
cp pastebin-app /etc/nginx/sites-enabled/default

# check configuration
nginx -t

# reload
service nginx reload
```
