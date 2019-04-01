# armNN on PYNQ/Ultra96 #

https://github.com/ARM-software/armnn

https://github.com/ARM-software/armnn/blob/branches/armnn_19_02/BuildGuideCrossCompilation.md


## Native Build ##
Try it on Ultra96 w/ Pynq v2.3. The Pynq v2.3 image is base on Ubuntu18.04.

Refer to  **[Cross-Compile ArmNN on x86_64 for arm64](https://community.arm.com/developer/tools-software/graphics/f/discussions/12066/cross-compile-armnn-on-x86_64-for-arm64)** 


Here is the script [build-armnn.sh](https://github.com/ARM-software/Tool-Solutions/tree/master/ml-tool-examples/build-armnn) can do the build.

Ultar96 use Xilinx Zynq MPSoC which integrate Mali400 which do not support OpenCL. 

    ./build-armnn.sh -a arm64-v8a -o 0

The build-armnn.sh will check current platform to do cross-compile or nativa-compile. It will dowloand many dependent packages that you should make sure the internet is avaliable.

The working directory tree is bellow here.

    xilinx@pynq:~$ tree -L 2 armnn-devenv
    armnn-devenv
    ├── ComputeLibrary
    │   ├── arm_compute
    │   ├── build
    │   ├── data
    │   ├── docs
    │   ├── documentation
    │   ├── documentation.xhtml
    │   ├── examples
    │   ├── include
    │   ├── LICENSE
    │   ├── opencl-1.2-stubs
    │   ├── opengles-3.1-stubs
    │   ├── README.md
    │   ├── SConscript
    │   ├── SConstruct
    │   ├── scripts
    │   ├── src
    │   ├── support
    │   ├── tests
    │   └── utils
    ├── gator
    │   ├── Acknowledgements.md
    │   ├── annotate
    │   ├── Contributing.md
    │   ├── daemon
    │   ├── dco.txt
    │   ├── driver
    │   ├── hrtimer_module
    │   ├── Maintainers.md
    │   ├── notify
    │   ├── pom.xml
    │   ├── python
    │   ├── README.md
    │   └── setup
    └── pkg
	    ├── boost
	    ├── install
	    ├── protobuf
	    └── tensorflow

The nativa-compile on Ultra96 take about 3 hours. You may see the log below means the compile is finished well.

    [100%] Built target UnitTests
    ~/armnn-devenv
    done, everything in armnn-devenv/
    xilinx@pynq:~$

The build output of Arm ComputeLibrary are at

    $ tree -L 2 ~/armnn-devenv/ComputeLibrary/build/
    /home/xilinx/armnn-devenv/ComputeLibrary/build/
    ├── libarm_compute_core.so
    ├── libarm_compute_core-static.a
    ├── libarm_compute_graph.so
    ├── libarm_compute_graph-static.a
    ├── libarm_compute.so
    ├── libarm_compute-static.a


The 3rd dependency stuffs are at

    $ tree -L 2 ~/armnn-devenv/pkg/install/lib/
    /home/xilinx/armnn-devenv/pkg/install/lib/
    ├── libprotobuf.a
    ├── libprotobuf.la
    ├── libprotobuf-lite.a
    ├── libprotobuf-lite.la
    ├── libprotobuf-lite.so -> libprotobuf-lite.so.15.0.1
    ├── libprotobuf-lite.so.15 -> libprotobuf-lite.so.15.0.1
    ├── libprotobuf-lite.so.15.0.1
    ├── libprotobuf.so -> libprotobuf.so.15.0.1
    ├── libprotobuf.so.15 -> libprotobuf.so.15.0.1
    ├── libprotobuf.so.15.0.1
    ├── libprotoc.a
    ├── libprotoc.la
    ├── libprotoc.so -> libprotoc.so.15.0.1
    ├── libprotoc.so.15 -> libprotoc.so.15.0.1
    ├── libprotoc.so.15.0.1
    └── pkgconfig
    ├── protobuf-lite.pc
    └── protobuf.pc

    
The output of armNN build are at 

    $ tree -L 2 ~/armnn-devenv/armnn/build/
    /home/xilinx/armnn-devenv/armnn/build/
    ├── CMakeCache.txt
    ├── CMakeFiles
    │   ├── 3.10.2
    │   ├── AdditionalCMakeFiles.dir
    │   ├── armnn.dir
    │   ├── armnnTfParser.dir
    │   ├── armnnUtils.dir
    │   ├── cmake.check_cache
    │   ├── CMakeDirectoryInformation.cmake
    │   ├── CMakeError.log
    │   ├── CMakeOutput.log
    │   ├── CMakeTmp
    │   ├── feature_tests.bin
    │   ├── feature_tests.c
    │   ├── feature_tests.cxx
    │   ├── Makefile2
    │   ├── Makefile.cmake
    │   ├── progress.marks
    │   ├── TargetDirectories.txt
    │   └── UnitTests.dir
    ├── cmake_install.cmake
    ├── libarmnn.so
    ├── libarmnnTfParser.so
    ├── libarmnnUtils.a
    ├── Makefile
    ├── samples
    │   ├── CMakeFiles
    │   ├── cmake_install.cmake
    │   └── Makefile
    ├── src
    │   └── backends
    └── UnitTests


## Run SimpleSample on Ultar96 ##
There is a very simple sample in A simple example of using the ArmNN SDK API. In this sample, the users single input number is multiplied by 1.0f using a fully connected layer with a single neuron to produce an output number that is the same as the input.

The source code is ~/armnn-devenv/armnn/samples/SimpleSample.cpp. 

### Compile ###
    
    $cd ~/armnn-devenv/armnn/samples/
    
    $g++ -O3 -std=c++17 SimpleSample.cpp -o SimpleSample \
    -I/home/xilinx/armnn-devenv/armnn/include -I/home/xilinx/armnn-devenv/pkg/boost/install/include \
    -L/home/xilinx/armnn-devenv/armnn/build -larmnn -larmnnTfParser -lpthread

### Run ###

    $ export LD_LIBRARY_PATH=:/home/xilinx/armnn-devenv/armnn/build
    $ ./SimpleSample
    Please enter a number:
    1
    Your number was 1
    xilinx@pynq:~/armnn-devenv/armnn/samples$


## Tensorflow MINST Demo ##
Download the demo project from [here](https://github.com/ARM-software/Tool-Solutions/tree/master/ml-tool-examples/mnist-demo). 

Suppose you put the project at ~/minst-demo/


    xilinx@pynq:~/mnist-demo$ make test
    g++ -O3 -std=c++17 mnist_tf_simple.cpp -o mnist_tf_simple \
    -I/home/xilinx/armnn-devenv/armnn/include -I/home/xilinx/armnn-devenv/pkg/boost/install/include \
    -L/home/xilinx/armnn-devenv/armnn/build -larmnn -larmnnTfParser -lpthread
    g++ -O3 -g -std=c++17 mnist_tf_convol.cpp -o mnist_tf_convol \
    -I/home/xilinx/armnn-devenv/armnn/include -I/home/xilinx/armnn-devenv/pkg/boost/install/include \
    -L/home/xilinx/armnn-devenv/armnn/build -larmnn -larmnnTfParser -lpthread
    LD_LIBRARY_PATH=:/home/xilinx/armnn-devenv/armnn/build ./mnist_tf_simple 1 10
    Warning gator_func(/home/xilinx/armnn-devenv/gator/annotate/streamline_annotate.c:496): Not connected to gatord, the application will run normally but Streamline will not collect annotations. To collect annotations, please verify you are running gatord 5.24 or later and that SELinux is disabled.
    Optimisation mode: CpuAcc
    #1 | Predicted: 7 Actual: 7
    #2 | Predicted: 2 Actual: 2
    #3 | Predicted: 1 Actual: 1
    #4 | Predicted: 0 Actual: 0
    #5 | Predicted: 4 Actual: 4
    #6 | Predicted: 1 Actual: 1
    #7 | Predicted: 4 Actual: 4
    #8 | Predicted: 9 Actual: 9
    #9 | Predicted: 6 Actual: 5
    #10 | Predicted: 9 Actual: 9
    Prediction accuracy: 90%
    LD_LIBRARY_PATH=:/home/xilinx/armnn-devenv/armnn/build ./mnist_tf_convol 1 10
    Warning gator_func(/home/xilinx/armnn-devenv/gator/annotate/streamline_annotate.c:496): Not connected to gatord, the application will run normally but Streamline will not collect annotations. To collect annotations, please verify you are running gatord 5.24 or later and that SELinux is disabled.
    Optimisation mode: CpuAcc
    #1 | Predicted: 7 Actual: 7
    #2 | Predicted: 2 Actual: 2
    #3 | Predicted: 1 Actual: 1
    #4 | Predicted: 0 Actual: 0
    #5 | Predicted: 4 Actual: 4
    #6 | Predicted: 1 Actual: 1
    #7 | Predicted: 4 Actual: 4
    #8 | Predicted: 9 Actual: 9
    #9 | Predicted: 5 Actual: 5
    #10 | Predicted: 9 Actual: 9
    Prediction accuracy: 100%
    xilinx@pynq:~/mnist-demo$

You may start the gatord before running the Demo or skip the Warning about gatro.

    /home/xilinx/armnn-devenv/gator/daemon/gatord &

You can try run.sh or mnist_tf_convol and mnist_tf_simple after the compiled.


----------

## Reference & Resource ##

https://github.com/ARM-software/Tool-Solutions

https://github.com/ARM-software/ML-examples/tree/master/armnn-mnist

https://developer.arm.com/products/processors/machine-learning/arm-nn

https://developer.arm.com/technologies/machine-learning-on-arm/developer-material/how-to-guides

https://community.arm.com/developer/tools-software/graphics/f/discussions/12066/cross-compile-armnn-on-x86_64-for-arm64

[How to Cross-Compile ArmNN on x86_64 for arm64](https://github.com/ARM-software/armnn/blob/branches/armnn_19_02/BuildGuideCrossCompilation.md)

[Deploying a Caffe MNIST model using the Arm NN SDK](https://developer.arm.com/technologies/machine-learning-on-arm/developer-material/how-to-guides/deploying-a-caffe-mnist-model-using-the-arm-nn-sdk/deploying-a-caffe-mnist-model-using-the-arm-nn-sdk-single-page)