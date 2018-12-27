# Docker Run Alveo U200 #

**Version 1.0**

**Author: Alex He <ahe@xilinx.com>**

**Date: 12/27/2018**


----------

Xilinx Launch the New Generation Adaptable Accelerator Cards, Alveo, for Data Center Worklaods at 2018 XDF. 

Please access here for more informaion at 
> https://www.xilinx.com/products/boards-and-kits/alveo.html

Xilinx support running Alveo at Redhat/CentOS/Ubuntu directly. This blog just show how to extend the deployment of Alveo by Docker. I use Alveo U200 and Xilinx Runtime(XRT) v2018.2 here.


**My Environments**

- Ubuntu16.04 in Host PC
- Ubuntu16.04 in Docker Image
- Alveo U200 and XRT v2018.2


**NOTE: The docker support of Alveo is not offical until now**

## Base Environment

You can build the docker image from pure Ubuntu from dockerhub (https://hub.docker.com/_/ubuntu). But I chose using the Nvidia-docker and bvlc/caffe:gpu(ubuntu16.04, caffe v1.0.0) since I could save time and leverage my Nvidia-GPU do more Machine Learning things(Training).

You need to install docker. If you want to use GPU do Machine Learning Training you need to replace docker with docker-ce and install Nvidia GPU driver, Nvidia-docker and cuDNN, etc. These things are not covered in this topic but you can find reference from Nvidia Original Webpage.

**Example**

Build and run bvlc/caffe:gpu docker image.

    $nvidia-docker run -ti bvlc/caffe:gpu --name ml-suite --version

*Please got to <https://github.com/BVLC/caffe/tree/master/docker> for more details


**Or** create a base container from a CPU&caffe Docker image

    $docker run -ti bvlc/caffe:cpu caffe --version

**Or** base on a pure Ubuntu16.04 Docker Image if you want install everything from scratch.

    $docker run -ti ubuntu:16.04 --version


Let's continue my trying with bvlc/caffe:gpu(ubuntu16.04, caffe v1.0.0) docker image.

Commit the container as docker image and name it **ml-suite**.
    
    $ sudo docker commit  -a "Alex He" -m "ml-suite base image with caffe_gpu" [Container ID] ml-suite

     * Please replace the [Container ID] got by "sudo docker ps -a"

Then let's use the "**ml-suite**" image to start ourjourney of  Machine Learning



## Install XRT in Host
Please install the Alveo U200 Xilinx Runtime(XRT) package v2018.2 from <https://www.xilinx.com/products/boards-and-kits/alveo/u200.html#2018_2>. The XRT include the PCIE device driver which export two device nodes of Alveo U200.
Dowload it and install the XRT deb. 

Refer to UG1301 to install dependencies.

The **Development Shell** of Alveo U200 also can be download from here. We will install XRT and Development Shell packages in Docker Container later.


I download the XRT and Development Shell deb packages in /DATA/Xilinx/x_u200/ of HOST and will be map to /data/Xilinx/x_u200/ in container.

The real name may have a minor changes with the NUMBER of device name.

Like my enviroments.

- /dev/xclmgmt1025
- /dev/dri/renderD129

## Start the Container

We should export the two device nodes of Alveo U200 into container by use "--device" option.


    $sudo docker run -it --name ml-suite-1 -d -v /DATA:/data --device=/dev/dri/renderD129:/dev/dri/renderD129 \
    --device=/dev/xclmgmt1025:/dev/xclmgmt1025 -p 9901:5901  --hostname=ml-suite --network=host \
     ml-suite:latest /bin/bash

I map /DATA directory of host to /data directory of container for sharing XRT and Development Shell packages of Alveo U200 between them.

**[Option]** You can use --network=bridge to run the docker. 
Network bridge is the default setting of container. You may need to set DNS of this bridge network mode acording to your LAN.
    
    $sudo docker run -it --name ml-suite-1 -d -v /DATA:/data --device=/dev/dri/renderD129:/dev/dri/renderD129 \ 
    --device=/dev/xclmgmt1025:/dev/xclmgmt1025 -p 9901:5901 --hostname=ml-suite --network=bridge \
    --dns=172.22.160.151 ml-suite:latest /bin/bash


## Install XRT and Development Shell in Container

Login to the running docker container.

    Check the container ID (which IMAGE named ml-suite-1) by,
    $sudo docker ps -a

    Replace your real Container ID in the command below,
    $sudo docker exec -it [Container ID] /bin/bash

### Install dependency packages

Refer to UG1301 to install dependencies

Install dependencies

    root@ml-suite:/data/Xilinx/x_u200# ./xrtdeps_container.sh
    root@ml-suite:/data/Xilinx/x_u200# apt-get -f install

**NOTE:**
After install the XRT in the HOST. You will got the /opt/xilinx/xrt/bin/xrtdeps.sh. This script help to install all the depenedent packages of XRT. We copy it as xrtdeps_container.sh and delete the "sudo" in command line since we already login the container as root.


I download the XRT and Development Shell deb packages in /DATA/Xilinx/x_u200/ of HOST and will be at /data/Xilinx/x_u200/ in container.

### Install XRT deb

    root@ml-suite:/data/Xilinx/x_u200# dpkg -i xrt_201802.2.1.83_16.04.deb


### Install Development Shell deb


    root@ml-suite:/data/Xilinx/x_u200# dpkg -i xilinx-u200-xdma-16.04.deb


### Check Development Shell and XRT

Show the installation directory

    root@ml-suite:/data/Xilinx/x_u200# tree /opt/xilinx/ -L 2
    /opt/xilinx/
    |-- dsa
    |   `-- xilinx_u200_xdma_201820_1
    `-- xrt
    |-- bin
    |-- include
    |-- lib
    |-- license
    |-- setup.csh
    |-- setup.sh
    `-- share
    
    8 directories, 2 files


### Run test with xbutil ###

Source the environment settings

    root@ml-suite:/data/Xilinx/x_u200# source /opt/xilinx/xrt/setup.sh

    xbutil list
    xbutil scan
    xbutil query
    xbutil validate

## Backup the Container ##

Commit the Container with the Alveo XRT/Development Shell Container installed to the Docker Image like this(run in HOST),


    $ sudo docker commit  -a "Alex He" -m "install XRT and Development Shell" 73ab0ee64280 ml-suite:1.0


Then you can start new work base on this Docker Image.

Or export the Container as a Image tar file could be share with ohters. Run in HOST and replace the Container ID as yours.

    $sudo docker export -o ml-suite-1.0.tar 73ab0ee64280
    

## Reference ##
- Xilinx UG1301 - Getting Started with Alveo Data Center Accelerator Cards
- [Docker Document ](https://docs.docker.com/reference/)
