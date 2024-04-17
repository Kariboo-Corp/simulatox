# Project Setup Guide

This guide covers the necessary steps for setting up the project environment using Docker.
This includes cloning the repository, installing Docker, and running a Docker container.

## Cloning the Repository

Before setting up Docker and building your container, you need to clone the project repository from GitHub.
This will provide you with all the necessary files, including the Dockerfile and source code.

1. **Open a Terminal**: Launch your terminal application.

2. **Navigate to the Desired Directory**: Use the `cd` command to navigate to the directory where you want to clone the repository.

   Example:

   ```bash
   cd path/to/your/directory
   ```

3. **Clone the Repository**: Run the following git command to clone the repository:

   ```bash
   git clone https://github.com/Kariboo-Corp/simulatox.git
   ```

   This command will create a folder named `simulatox` in your current directory and download the contents of the repository into it.

4. **Navigate to the Repository Directory**: After cloning, move into the repository directory:

   ```bash
   cd simulatox
   ```

Now that you have the repository cloned, you can proceed with the Docker setup as per the following sections.

## Installing Docker, and running a Docker container

This guide provides instructions on setting up Docker and running a container for our project.

### Installing Docker

- Docker installed on your system. Follow the official Docker documentation for your specific
  Linux distribution to install Docker. Finally make sure that your

- **Check Docker Service Status**

  ```bash
  systemctl status docker
  ```

  This command checks the current status of the Docker service.

- **Start Docker Service**

  ```bash
  sudo systemctl start docker
  ```

  Use this command to start the Docker service if it is not running.

- **Enable Docker Service on Boot**
  ```bash
  sudo systemctl enable docker
  ```
  This will configure Docker to start automatically at system boot.

### Building the Docker Container

Once you have cloned the `simulatox` repository, the next step is to build the Docker container. This process involves
creating a Docker image from the Dockerfile in the repository, which contains all the necessary configurations and dependencies.

1. **Navigate to the Repository Directory**: Ensure that you are in the root directory of the `simulatox` repository.
   This is where the Dockerfile should be located.

   ```bash
   cd path/to/simulatox
   ```

2. **Build the Docker Image**: Use the following command to build the Docker image.
   This command creates an image with the tag `pfa`, using the Dockerfile in the current directory (`.`).

   ```bash
   sudo docker image build . -t pfa
   ```

   - `sudo`: Runs the command with superuser privileges.
   - `docker image build`: Docker command to build an image.
   - `.`: Specifies the current directory as the build context where Docker looks for the Dockerfile.
   - `-t pfa`: Tags the created image with the name `pfa` for easy identification.

3. **Allow X11 Connections**: If your application requires a GUI and uses the host's X11 server, run the following command:

   ```bash
   xhost +
   ```

   This command configures the X server to allow connections from any client.
   This step is crucial for GUI applications running in Docker containers to display correctly on your host machine.

### Starting the Container

To start a Docker container:

1. **Run the Container**: Use the `docker run` command to start the container with specific options:

   ```bash
   sudo docker run -d -it --rm -p 127.0.0.1:8000:8000 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/dri:/dev/dri -v ./src:/PROJECT --name my_container pfa
   ```

   Here's a breakdown of this command:

   - `-d`: Runs the container in **detached mode**, meaning it runs in the background.
     You can continue to use the terminal while the container is running.

   - `-it`: This flag combines `-i` and `-t`. `-i` keeps **STDIN open** even if not attached,
     and `-t` allocates a **pseudo-TTY**. This combination is useful for interactive sessions.

   - `--rm`: Automatically **removes** the container when it exits.
     This is useful for cleaning up and not leaving behind any stopped containers.

   - `-p 127.0.0.1:8000:8000`: Forwards port 8000 from the container to port 8000 on the host, but only accessible from the localhost.

   - `-e DISPLAY=$DISPLAY`: Sets an **environment variable** inside the container. In this case, it's passing the `DISPLAY` environment
     variable from your host to the container, which is essential for GUI applications to display correctly.

   - `-v /tmp/.X11-unix:/tmp/.X11-unix`: Mounts a **volume**. This specific command mounts the X11 UNIX socket
     from the host into the container, allowing GUI applications in the container to use the host’s display.

   - `--device=/dev/dri:/dev/dri`: Grants the container access to a **specific device**. This is often used for
     granting GPU access to the container, which can be necessary for applications that require hardware acceleration.

   - `-v ./src:/PROJECT`: Another volume mount, mapping a local directory (`./src`) to a directory inside
     the container (`/PROJECT`). This allows for sharing files between the host and the container.

   - `--name my_container`: Assigns a **custom name** (`my_container`) to the container. This makes it easier
     to reference the container in subsequent Docker commands.

   - `pfa`: The **name of the image** to run as a container.

2. **Customize the Run Command**: Depending on your application's needs, you might need to customize this command further,
   for example, by mapping ports, volumes, or setting environment variables.

### Accessing the Container

To interact with a running container:

- **Accessing the Shell**: If you need to enter the container’s shell (bash), use the `docker exec` command:

  ```bash
  sudo docker exec -it my_container /bin/bash
  ```

### Stopping the Container

When you’re done, you can stop the container:

- **Stop the Container**: Use the `docker stop` command:

  ```bash
  sudo docker stop my_container
  ```

### Listing Containers and Images

To keep track of your containers and images, you can list them using the following commands:

- **List Containers**:
  For active containers:

  ```bash
  docker ps
  ```

  For all containers, including stopped ones:

  ```bash
  docker ps -a
  ```

- **List Images**:
  To see all Docker images on your system:

  ```bash
  docker images
  ```

## Cleaning

### Removing Unused Containers

After stopping a container, you can remove it to free up disk space:

```bash
docker rm [CONTAINER_ID or CONTAINER_NAME]
```

Replace `[CONTAINER_ID or CONTAINER_NAME]` with the ID or name of your container. Find this information by using `docker ps -a`.

### Removing Unused Images

Docker images can occupy a significant amount of disk space. To remove an unused image:

```bash
docker rm [CONTAINER_ID or CONTAINER_NAME]
```

Replace `[IMAGE_ID or IMAGE_NAME]` with the ID or name of the image. Use `docker images` to view all available images.

### Automatically Cleaning Up Unused Resources

Docker provides a handy command to remove unused containers, networks, volumes, and images:

```bash
docker system prune
```

This command will remove all unused resources. To also include unused images, use:

```bash
docker system prune -a
```

### Managing Orphaned Volumes

Volumes not attached to any containers can also occupy space. To remove them:

```bash
docker volume prune
```

### Global Cleanup:

For a more comprehensive cleanup, including stopped containers, unused images, orphaned volumes, and unused networks:

```bash
docker system prune -a
```

This command will thoroughly clean up your Docker environment. It removes all stopped containers, unused images (both dangling and unreferenced by any container), unused volumes, and networks not used by at least one container.

Remember, using this command might result in data loss if any important information is stored in these containers or images. Make sure to back up any necessary data before proceeding.
