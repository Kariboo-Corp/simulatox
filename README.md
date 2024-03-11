# PFA

## Requirements
- Install Docker


## Build & Launch container

```
❯ sudo docker image build . -t ros2
❯ xhost +

```

## On Fedora
```
❯  sudo  docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ./src:/PROJECT --device=/dev/dri:/dev/dri ros2
```


```
Quentin : 

sudo docker run -d -it --rm --device=/dev/dri:/dev/dri -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ./PROJECT:/PROJECT mon_image_pfa

docker exec -it <container_id> bash # Where <container_id> is the result of the last command

docker ps # To obtain <container_id> if you've lost it
```
