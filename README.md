# PFA

## Requirements
- Install Docker


## Build & Launch container

```
❯ sudo docker image build . -t ros2
❯ xhost +
❯ sudo  docker run -it --rm -e DISPLAY=$DISPLAY -v ./src:/PROJECT ros2
```