# Use nvidia-docker-run-digits #

https://github.com/NVIDIA/nvidia-docker 

Follow the guide([NVIDIA Container Runtime for Docker](https://github.com/NVIDIA/nvidia-docker )) to install 

It works for me follow the steps


### Prerequisites ###

The **QUICKSTART** in https://github.com/NVIDIA/nvidia-docker show some prerequisites

1. GNU/Linux x86_64 with kernel version > 3.10
1. Docker CE >= 1.12
1. NVIDIA GPU with Architecture > Fermi (2.1)
1. NVIDIA drivers ~= 361.93 (untested on older versions)
1. CUDA 

**NOTE** Your driver version might limit your CUDA capabilities (see [CUDA requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements))


## Install ##

**QUICKSTART**

Make sure you have installed the NVIDIA driver and a supported version of Docker for your distribution (see prerequisites).

If you have a custom /etc/docker/daemon.json, the nvidia-docker2 package might override it.

Ubuntu 14.04/16.04/18.04, Debian Jessie/Stretch

    # If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
    docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
    sudo apt-get purge -y nvidia-docker
    
    # Add the package repositories
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
      sudo apt-key add -
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
      sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt-get update
    
    # Install nvidia-docker2 and reload the Docker daemon configuration
    sudo apt-get install -y nvidia-docker2
    sudo pkill -SIGHUP dockerd
    
    # Test nvidia-smi with the latest official CUDA image
    docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi



## Use it ##

### Basic Usage ###

nvidia-docker registers a new container runtime to the Docker daemon.
 You must select the nvidia runtime when using docker run:

    docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi

Bellow is the infomation about my enviroments.

    $ sudo docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi
    Unable to find image 'nvidia/cuda:9.0-base' locally
    9.0-base: Pulling from nvidia/cuda
    18d680d61657: Pull complete
    0addb6fece63: Pull complete
    78e58219b215: Pull complete
    eb6959a66df2: Pull complete
    6ef1ff668c93: Pull complete
    f5f8f0544aa2: Pull complete
    3d28d96eb352: Pull complete
    Digest: sha256:764039ce9ff2cfb44d646fde6930099493334bb743e5b4f089d820de023c5d9a
    Status: Downloaded newer image for nvidia/cuda:9.0-base
    Wed Nov 21 03:37:25 2018
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 410.72   Driver Version: 410.72   CUDA Version: 10.0 |
    |-------------------------------+----------------------+----------------------+
    | GPU  NamePersistence-M        | Bus-IdDisp.A         | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap| Memory-Usage         | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  Quadro K620 Off          | 00000000:03:00.0  On |  N/A                 |
    | 34%   41CP8 1W /  30W         | 52MiB /  2000MiB     |  1%  Default         |
    +-------------------------------+----------------------+----------------------+
    
    +-----------------------------------------------------------------------------+
    | Processes:   GPU Memory                                                     |
    |  GPU   PID   Type   Process name Usage                                      |
    |=============================================================================|
    +-----------------------------------------------------------------------------+


### Advance Usage ###

There is a very good project in github to guide you use Nvidia DIGITS in docker to train a Caffe model.

https://github.com/humphd/have-fun-with-machine-learning 

It has a very sweet README to lead you train a model step-by-step. 

**BUT**

It just show use CPU-only docker image to do that which is very slowly. So if you have NVIDIA GPU has capablity of speed up. You'd like to try levelage the GPU with nvidia-docker. 

Here is the example.

Start the nvidia-docker images.

    $sudo nvidia-docker run --name digits5 -d -p 9090:5000 -v /DATA/Gits/have-fun-with-machine-learning:/data/repo nvidia/digits:5.0

You must note that we still use the data(image data for training model) got from https://github.com/humphd/have-fun-with-machine-learning . 

Other things about do the training model is same as description in https://github.com/humphd/have-fun-with-machine-learning 

As my experience to train a same model with same data, the nvidia-docker w/ gpu may be 30times fast than docker w/o gpu. 


----------

### Reference ###

    https://github.com/NVIDIA/nvidia-docker  
    https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0)