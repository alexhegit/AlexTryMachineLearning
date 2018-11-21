# Install Caffe #

You know **Install Caffe** is one thing you never try second time. This blog record the key points about How-To install Caffe on my PC/Ubuntu16.04. Hope it will help when you do it and only need do it one time. 

Good Luck!

## My Enviroment ##
**DELL T5810**

- Ubuntu 16.04 x86_64 w/ linux kernel 4.15.0-39-generic
- anacond3 v4.5.1 w/ python3.6
- Nvidia Quadra K620 (2GB)
- Intel(R) Xeon(R) CPU E5-1603 v3 @ 2.80GHz
- 64GB DDR4


## Installation ##

There are many way to depoly the Caffe. I will show you build the Caffe base on anaconda with GPU and OpenCV.

- opencv
- pycaffe
- CUDA10/cuDNN/nvidia dirver-410

### Dependency Packages  ###

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y build-essential cmake git pkg-config
    sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev protobuf-compiler
    
    sudo apt-get install -y libatlas-base-dev 
    sudo apt-get install -y --no-install-recommends libboost-all-dev
    
    sudo apt-get install -y libgflags-dev libgoogle-glog-dev liblmdb-dev
    sudo apt-get -y install build-essential cmake git libgtk2.0-dev pkg-config python-dev python-numpy libdc1394

### Install staffs for Nvidia GPU ###
Caffe can work at CPU-only mode but very slowly. You can enable GPU for running caffe to save you life. For that, you need install Nvidia driver/cuDNN/CUDA first.



#### Install Nvidia driver ####

    sudo apt-get install -y nvidia-410 nvidia-410-dev

I install v410 for my GPU card. You need to decide which version driver base on your GPU and which version CUDA you want. This is a little complex things to chose the version of them. I advice to get more information from 

[https://developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus)

[https://en.wikipedia.org/wiki/CUDA](https://en.wikipedia.org/wiki/CUDA)




#### Install CUDA  ####
Download CUDA from [Nvidia Developer Zone](https://developer.nvidia.com/cuda-downloads)

*You may need register a account first.*

CUDA support Windows, Linux and MacOS. I download **Linux x86_64 Ubuntu 16.04 deb ** package for my hardware platform. I skip the details of the installation.

To verify the CUDA and driver installation

    $ nvcc --version
    nvcc: NVIDIA (R) Cuda compiler driver
    Copyright (c) 2005-2018 NVIDIA Corporation
    Built on Sat_Aug_25_21:08:01_CDT_2018
    Cuda compilation tools, release 10.0, V10.0.130
    
    $nvidia-smi
    Tue Nov 20 15:00:10 2018
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 410.72   Driver Version: 410.72   CUDA Version: 10.0             |
    |-------------------------------+----------------------+----------------------+
    | GPU  NamePersistence-M        | Bus-IdDisp.A         | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap| Memory-Usage         | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  Quadro K620 Off          | 00000000:03:00.0  On |  N/A                 |
    | 34%   40CP8 1W /  30W         | 52MiB /  2000MiB     |  0%  Default         |
    +-------------------------------+----------------------+----------------------+
    
    +-----------------------------------------------------------------------------+
    | Processes:   GPU Memory                                                     |
    |  GPU   PID   Type   Process name Usage                                      |
    |=============================================================================|
    |0   970  G   /usr/lib/xorg/Xorg49MiB                                         |
    +-----------------------------------------------------------------------------+


#### Install cuDNN ####
Downloand cuDNN from [https://developer.nvidia.com/rdp/cudnn-download](https://developer.nvidia.com/rdp/cudnn-download)

Chose the version base on your platform. For me I download the deb packages of Ubuntu16.04 x86_64/CUDA-10.

    $ls /DATA/ML/NVIDIA/cuDNN_7.3.1/
    libcudnn7_7.3.1.20-1+cuda10.0_amd64.deb  libcudnn7-doc_7.3.1.20-1+cuda10.0_amd64.deb
    libcudnn7-dev_7.3.1.20-1+cuda10.0_amd64.deb

   Use dpkg to install them.




### Install Anaconda3 ###

It is very easy to install anaconda. You just need to [download installation file](https://www.anaconda.com/download/)(.sh) it and run it to finish the installation. I install it at "~/anaconda3".

Then you need use conda install many packages

    conda install -c menpo opencv3
    conda install libgcc
    conda install protobuf
    conda install libboost

And modify the ~/.bashrc add these lines. 

    # add for Anaconda3
    export PATH="/home/ahe/anaconda3/bin:$PATH"
    export LD_LIBRARY_PATH=/home/ahe/anaconda3/lib:$LD_LIBRARY_PATH
    export CPLUS_INCLUDE_PATH=/home/ahe/anaconda3/include/python3.6m
    
    # add for CUDA
    export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
    export LIBRARY_PATH=/usr/local/cuda/lib64${LIBRARY_PATH:+:${LIBRARY_PATH}}


### Install the caffe ###
The diffical part is compile the caffe. 

Please download it from github [/BVLC/caffe](https://github.com/BVLC/caffe)

    $git clone https://github.com/BVLC/caffe.git
    $cd [pathto]/caffe
    $cp Makefile.config.example Makefile.config


Install the dependencies with


    for req in $(cat requirements.txt); do pip install $req; done


Then modify the Makefie.config as required(enable GPU/CUDNN, etc). I paste the difference what I do here.

    $ diff Makefile.config.example Makefile.config
    2a3,5
    > #
    >
    > #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
    5c8
    < # USE_CUDNN := 1
    ---
    > USE_CUDNN := 1
    23c26
    < # OPENCV_VERSION := 3
    ---
    > OPENCV_VERSION := 3
    39,41c42
    < CUDA_ARCH := -gencode arch=compute_20,code=sm_20 \
    <   -gencode arch=compute_20,code=sm_21 \
    <   -gencode arch=compute_30,code=sm_30 \
    ---
    > CUDA_ARCH :=  -gencode arch=compute_30,code=sm_30 \
    71c72
    < PYTHON_INCLUDE := /usr/include/python2.7 \
    ---
    > # PYTHON_INCLUDE := /usr/include/python2.7 \
    75,78c76,79
    < # ANACONDA_HOME := $(HOME)/anaconda
    < # PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
    <   # $(ANACONDA_HOME)/include/python2.7 \
    <   # $(ANACONDA_HOME)/lib/python2.7/site-packages/numpy/core/include
    ---
    > ANACONDA_HOME := $(HOME)/anaconda3
    > PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
    >$(ANACONDA_HOME)/include/python3.6m \
    >$(ANACONDA_HOME)/lib/python3.6/site-packages/numpy/core/include
    81c82
    < # PYTHON_LIBRARIES := boost_python3 python3.5m
    ---
    > PYTHON_LIBRARIES := boost_python3 python3.6m
    83c84
    < # /usr/lib/python3.5/dist-packages/numpy/core/include
    ---
    > #  /usr/lib/python3.5/dist-packages/numpy/core/include
    86,87c87,88
    < PYTHON_LIB := /usr/lib
    < # PYTHON_LIB := $(ANACONDA_HOME)/lib
    ---
    > # PYTHON_LIB := /usr/lib
    > PYTHON_LIB := $(ANACONDA_HOME)/lib
    94c95
    < # WITH_PYTHON_LAYER := 1
    ---
    > WITH_PYTHON_LAYER := 1
    97,99c98,103
    < INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
    < LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib
    <
    ---
    > #INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
    > #LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib
    > INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial
    > LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linu   x-gnu/hdf5/serial
    > #INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial
    > #LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-lin   ux-gnu/hdf5/serial
    120a125,128
    >
    > # Alex
    > #LINKFLAGS := -Wl,-rpath,/home/ubuntu/anaconda3/lib
    >

    


Now to build it

    $source ~/.bashrc
    $make all -j $(($(nproc) + 1))
    $make test -j $(($(nproc) + 1))
    $make runtest -j $(($(nproc) + 1))
    $make pycaffe -j $(($(nproc) + 1))
    $ln -s [pathto]/caffe ~/caffe

**Build Issues**


- [enabled -std=c++11  #6359](https://github.com/BVLC/caffe/issues/6359)

Modify the Makefile to add -std=gnu++11 in these lines.

	CXXFLAGS += -pthread -fPIC $(COMMON_FLAGS) $(WARNINGS) -std=c++11
    NVCCFLAGS += -D_FORCE_INLINES -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS) -std=c++11
    LINKFLAGS += -pthread -fPIC $(COMMON_FLAGS) $(WARNINGS) -std=c++11

- [BatchReindexLayer fails GPU gradient tests under CUDA v9.1  #6164](https://github.com/BVLC/caffe/issues/6164)

- [Caffe make runtest error #5959](https://github.com/BVLC/caffe/issues/5959)

To import the caffe Python module after completing the installation, add the module directory to your $PYTHONPATH by export PYTHONPATH=/path/to/caffe/python:$PYTHONPATH or the like. You should not import the module in the caffe/python/caffe directory!

E.g. add PATH of caffe to ~/.bashrc
    
    # add caffe
    export CAFFE_ROOT=~/caffe
    export PYTHONPATH=~/caffe/python:$PYTHONPATH



### Docker run caffe ###

    https://hub.docker.com/r/bvlc/caffe/
    https://github.com/BVLC/caffe/tree/master/docker

Running an official image
You can run one of the automatic builds. E.g. for the CPU version:

docker run -ti bvlc/caffe:cpu caffe --version

or for GPU support (You need a CUDA 8.0 capable driver and nvidia-docker):

nvidia-docker run -ti bvlc/caffe:gpu caffe --version

You might see an error about libdc1394, ignore it.



----------
 

## Reference ##

[How to install CUDA](https://nvidia.custhelp.com/app/answers/detail/a_id/2136/~/how-to-install-cuda)

[cuDNN INSTALLATION](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html)

[Install caffe with anaconda(3.6) on ubuntu16.04](http://www.yaoingwen.com/ubuntu16-04-anaconda-3-6-caffe/)

[Installion Caffe/BVLC](http://caffe.berkeleyvision.org/installation.html)

https://zhuanlan.zhihu.com/p/29823232 



## Question ##
1. Install caffe by conda directly?

https://anaconda.org/anaconda/caffe-gpu

https://anaconda.org/anaconda/caffe



----------


> Alex He, 11/21/2018 10:48:24 AM 
>
> Edit by MarkdownPad2