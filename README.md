# PFA

## Requirements
- Install Docker


## Build & Launch container

```
❯ sudo docker image build . -t ros2
❯ xhost +
❯ sudo  docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ros2
```