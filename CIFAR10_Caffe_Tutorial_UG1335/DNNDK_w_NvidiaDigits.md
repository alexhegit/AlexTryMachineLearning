# Use DNNDKwDIGITS by docker #

I push a docker [image](https://cloud.docker.com/u/alexhegit/repository/docker/alexhegit/dnndk) which have Xilinx DNNDK and NVIDIA DIGITS installed to the dockerhub. 

## Pull the docker image ##

>$docker pull alexhegit/dnndk:2.08_ditits6.1

## Start the Container ##

Two network mode for you reference to start the container.

### Host Network Mode ###

    $docker run --runtime=nvidia -it --network=host --name dnndk208 --hostname=dnndk -d -v /home/ahe/:/ahe  alexhegit/dnndk:2.08_digits6.1  /bin/bash

*NOTE: you may changing the options as your need *


## Start DIGITS Service ##
Login to the containner

    $ docker exec -it dnndk208 /bin/bash

Start the DIGITS Service

    $ /root/digits/digits-devserver -p 5000

## Login the DIGITS ##

Open the web browser and input the URL

http://localhost:5000 OR http://[host IP]:5000 at remote machine.


## Using the DIGITS ##

[[Here](https://docs.nvidia.com/deeplearning/digits/digits-user-guide/index.html)] is the offical user guide of NVIDIA/DIGITS.

## Training miniVggNet by DIGITS ##

Xilinx publish the [Edge AI Tutorials](https://github.com/Xilinx/Edge-AI-Platform-Tutorials) which give you some examples. You can follow the instructions and scripts to training the NN and using DNNDK to deploy them. At the training stage, the scripts is good way to know how it work in code. But DIGITS can give you a better visual view to watch how things going.

There is a guide for using DIGITS to train the miniVggNet which used in [CIFAR10 Caffe Tutorial, UG1335](https://github.com/Xilinx/Edge-AI-Platform-Tutorials/tree/master/docs/ML-CIFAR10-Caffe).

[[Here](https://github.com/alexhegit/AlexTryMachineLearning/blob/master/CIFAR10_Caffe_Tutorial_UG1335/Training_miniVggNet_by_NVIDIA%20DIGITS.pdf)]


## Reference ##
- https://github.com/Xilinx/Edge-AI-Platform-Tutorials
- https://github.com/NVIDIA/nvidia-docker/wiki/DIGITS
- https://docs.nvidia.com/deeplearning/digits/digits-release-notes/running-digits.html
- https://docs.nvidia.com/deeplearning/digits/pdf/DIGITS-Installation-Guide.pdf
- https://docs.nvidia.com/deeplearning/digits/digits-user-guide/index.html