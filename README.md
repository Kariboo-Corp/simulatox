# Project Setup Guide

> This guide covers the necessary steps for setting up the project environment using Docker.
This includes cloning the repository, installing Docker and running a Docker container.
> 

## I. Cloning the Repository

> Before setting up Docker and building your container, you need to clone the project repository from GitHub : ‣
This will provide you with all the necessary files, including the `Dockerfile` and source code.
> 
1. **Clone the Repository**: Run the following git command to clone the repository.
    
    <aside>
    <img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This command will create a folder named `simulatox` in your current directory and download the contents of the repository into it.
    
    ```bash
    git clone [https://github.com/Kariboo-Corp/simulatox.git](https://github.com/Kariboo-Corp/simulatox.git)
    ```
    
    </aside>
    
2. **Navigate to the Repository Directory**: After cloning, move into the repository directory.

Now that you have the repository cloned, you can proceed with the Docker setup as per the following sections.

## II. Installing Docker and Containers

### a. Installing Docker and start Docker Service

> Install Docker on your system. Follow the official Docker documentation for your specific Linux distribution to install Docker. If you intend to exploit the GPU's capabilities for certain tasks, install and configured the NVIDIA Container Toolkit.
> 
1. **Check Docker Service Status**
    
    <aside>
    <img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This command checks the current status of the Docker service.
    
    ```bash
    systemctl status docker
    ```
    
    </aside>
    
2. **Start Docker Service**
    
    <aside>
    <img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> Use this command to start the Docker service if it is not running.
    
    ```bash
    sudo systemctl start docker
    ```
    
    </aside>
    

### b. Building the Docker Container

> Once you have cloned the `simulatox` repository and start Docker Service , the next step is to build the Docker container. This process involves creating a Docker image from the `Dockerfile` in the repository, which contains all the necessary configurations and dependencies.
> 
1. **Navigate to the Repository Directory**: Ensure that you are in the root directory of the `simulatox` repository. This is where the `Dockerfile` should be located.
2. **Build the Docker Image**: Use the following command to build the Docker image.
    
    <aside>
    <img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This command creates an image with the tag `pfa`, using the Dockerfile in the current directory (`.`).
    
    ```bash
    sudo docker image build . -t pfa
    ```
    
    </aside>
    

### c. Listing Containers and Images

> To keep track of your containers and images, you can list them using the following commands:
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> List Containers :

- For active container.

```bash
docker ps
```

- For all containers, including stopped ones.

```bash
docker ps -a
```

</aside>

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> To see all Docker images on your system :

```bash
docker images
```

</aside>

## III Running the Container

### a. **Allow X11 Connections**

> The application requires a GUI and uses the host’s X11 server. This step is crucial for GUI applications running in Docker containers to display correctly on your host machine.
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This command configures the X server to allow connections from any client.

```bash
xhost +
```

- Consider adding a note about security best practices, especially when enabling X11 forwarding (**`xhost +`**). This command can make your system less secure by allowing any X11 client to connect to your display. A more secure alternative is to allow connections only from the Docker container:

```bash
xhost +local:docker
```

</aside>

### b. Run the container

> To start a Docker container, use the `docker run` command to start the container with specific options.
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This will start `my_container` from the `pfa` Docker Image.

```bash
sudo docker run -d -it --rm -p 127.0.0.1:8000:8000 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/dri:/dev/dri -v ./src:/PROJECT --name my_container pfa
```

- `-d` : Runs the container in **detached mode**, meaning it runs in the background. You can continue to use the terminal while the container is running.
- `-it`: This flag combines `-i` and `-t`. `-i` keeps **STDIN open** even if not attached,
and `-t` allocates a **pseudo-TTY**. This combination is useful for interactive sessions.
- `-rm`: Automatically **removes** the container when it exits. This is useful for cleaning up and not leaving behind any stopped containers.
- `-p 127.0.0.1:8000:8000`: Forwards port 8000 from the container to port 8000 on the host, but only accessible from the [localhost](http://localhost) for the front interface
- `-e DISPLAY=$DISPLAY`: Sets an **environment variable** inside the container. In this case, it’s passing the `DISPLAY` environment variable from your host to the container, which is essential for GUI applications to display correctly.
- `-v /tmp/.X11-unix:/tmp/.X11-unix`: Mounts a **volume**. This specific command mounts the X11 UNIX socket from the host into the container, allowing GUI applications in the container to use the host’s display.
- `--device=/dev/dri:/dev/dri`: Grants the container access to a **specific device**. This is often used for granting GPU access to the container, which can be necessary for applications that require hardware acceleration.
- `-v ./src:/PROJECT`: Another volume mount, mapping a local directory (`./src`) to a directory inside the container (`/PROJECT`). This allows for sharing files between the host and the container.
- `--name my_container`: Assigns a **custom name** (`my_container`) to the container. This makes it easier to reference the container in subsequent Docker commands.
- `pfa`: The **name of the image** to run as a container.
</aside>

Depending on your application’s needs, you might need to customize this command further, for example, by mapping ports, volumes, or setting environment variables. For instance, the **`DISPLAY`** variable helps the Docker container communicate with the host's X11 server for GUI applications.

### c. Accessing the Container

> To interact with a running container accessing the Shell
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This commande is used to access a running Docker container interactively. Here's a breakdown of each component of the command.

```bash
sudo docker exec -it my_container /bin/bash
```

</aside>

In this case, **`/bin/bash`** starts the Bash shell within the container, giving you a command-line interface to work with.

### d. Stopping the Container

> When you’re done, you can stop the container.
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> Use the `docker stop` command with the container `my_container`.

```bash
sudo docker stop my_container
```

</aside>

## IV. Cleaning

> Remember, using this command might result in data loss if any important information is stored in these containers or images. Make sure to back up any necessary data before proceeding.
> 

### a. Removing Unused Containers

> After stopping a container, you can remove it to free up disk space:
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> Replace `[CONTAINER_ID or CONTAINER_NAME]` with the ID or name of your container. Find this information by using `docker ps -a`.

```bash
docker rm [CONTAINER_ID or CONTAINER_NAME]
```

</aside>

### b. Removing Unused Images

> Docker images can occupy a significant amount of disk space. To remove an unused image:
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> Replace `[IMAGE_ID or IMAGE_NAME]` with the ID or name of the image. Use `docker images` to view all available images.

```bash
docker rmi [CONTAINER_ID or CONTAINER_NAME]
```

</aside>

### c. Managing Orphaned Volumes

> Volumes not attached to any containers can also occupy space. To remove them:
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This command will clean up your orphaned volumes.

```bash
docker volume prune
```

</aside>

### d. Global Cleanup:

> For a more comprehensive cleanup, including stopped containers, unused images, orphaned volumes, and unused networks:
> 

<aside>
<img src="https://www.notion.so/icons/command-line_gray.svg" alt="https://www.notion.so/icons/command-line_gray.svg" width="40px" /> This command will thoroughly clean up your Docker environment.

```bash
docker system prune
```

- When you add the `-a` or **`-all`** flag, the command removes all unused images not just dangling ones (i.e., images without tags or references). This includes images that are not referenced by any container, stopped or running.
</aside>

Future Enhancements
Docker Compose Integration:
For projects that scale to multiple containers or have complex service interactions, consider incorporating Docker Compose. This tool allows you to manage multi-container Docker applications through a single YAML file, simplifying configuration and operation processes. Docker Compose will enable you to start, stop, and rebuild services together and control how services are connected to each other.
Testing and Verification:
Include a section on testing the Docker setup to ensure everything is functioning as expected. This could involve:
Accessing a web interface at [http://localhost:8000](http://localhost:8000/) to confirm the web server is properly routed through Docker.
Running a command inside the container to verify the environment is correctly configured, such as docker exec -it [container_name] env.
Current Documentation and Comments
Existing Documentation:
Your repository includes README files in critical directories (src, etc.) and the Dockerfile is well-commented. This is excellent as it helps maintainers and new users understand the structure and logic of your application setup quickly.
Additional Recommendations
Version Pinning:
To ensure consistent, reliable builds and deployments, pin the versions of the base images in your Dockerfile. This prevents potential incompatibilities arising from unexpected updates to the base images used in your Docker environment.