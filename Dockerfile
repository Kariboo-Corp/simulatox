FROM ubuntu:22.04

ENV ROS_DISTRO humble
ENV DEBIAN_FRONTEND noninteractive


# Mettre à jour les packages et installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    lsb-release \
    wget \
    git \
    build-essential \
    ninja-build \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    gnupg \
    lsb-release

#Installer ROS2

RUN apt update && apt install locales && locale-gen en_US en_US.UTF-8 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && export LANG=en_US.UTF-8

RUN apt install software-properties-common && \
    add-apt-repository universe  && apt install -y tcl

RUN apt update && \
    apt install -y curl gnupg2 lsb-release && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt update && \
    apt install -y ros-$ROS_DISTRO-desktop



# Source ROS2
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc


RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
apt-get update && \
apt-get install gz-harmonic -y



#Installer dernière dépendance

RUN apt-get install -y \
    libgl1-mesa-glx && \
    pip install kconfiglib \
    symforce \
    pyros-genmsg \
    jsonschema \
    future \
    dash \
    pandas \
    dash-bootstrap-components
    


# Installer PX4
RUN git clone https://github.com/PX4/PX4-Autopilot.git && \
    cd PX4-Autopilot && make 

# Définir l'environnement pour PX4
ENV PX4_HOME_LAT 47.3765
ENV PX4_HOME_LON 8.5488
    
RUN pip install --quiet --no-input PEXPECT

#Installer Micro XRCE-DDS Agent
RUN git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git && \
    cd Micro-XRCE-DDS-Agent && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    ldconfig /usr/local/lib/

#Installer Rosdep et Colcon
RUN apt-get install -y \
    python3-rosdep \
    python3-colcon-common-extensions

#Utiliser bash au lieu de sh
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

#Installer et compiller px4_msgs
RUN mkdir -p /PX4-Autopilot/px4_packages/src &&\
    cd /PX4-Autopilot/px4_packages && \
    git clone https://github.com/PX4/px4_msgs.git && \
    cd /PX4-Autopilot/px4_packages && \
    source /opt/ros/humble/setup.bash && \
    colcon build

#Ajout de l'utilisateur dev
RUN useradd -r -p $(openssl passwd -1 1234) dev
RUN usermod -aG sudo dev
USER dev

#Port d'exposition pour le server web
EXPOSE 8000
