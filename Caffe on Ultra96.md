# Caffe on Ultra96 #

[https://github.com/alexhegit/AlexTryMachineLearning]
----------


## Installation ##

**http://www.pynq.io/  -download pynq image for Ultra96(I ust v2.3 here)**

**flash the image to SD card(suggest use 32GB)**

**Open gparted to increase the image size to full space**

**To link python3.6 to python3 in terminal(default setting already)**

**Install dependencies for caffe**
    
    $sudo apt-get upgrade
    $sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler   
    $sudo apt-get install --no-install-recommends libboost-all-dev libopenblas-dev
    $sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
    
    --all these file go in /usr/lib/aarch64-linux-gnu/(ultra96)

**Install Protobuf 3 using**

    $pip3 install numpy 
    $pip3 install protobuf


**Add SWAP USB**

    Since Ultra96 has limited RAM, in order to install Caffe extra memory will be required in the form of swap memory. In my test, a USB with size 2GB is large enough.
       
    $mkswap /dev/sda  
    $swapon /dev/sda
   
**Install Caffe**

	Clone or download caffe from link provided. This is for Caffe ssd model.
    	https://github.com/weiliu89/caffe/tree/ssd 
    	Backup git: https://github.com/dengdan/ssd-caffe
    
    Copy the PYNQ version of Makefile.config (provided under PYNQ-object-Detection/caffe-ssd/) to caffe root directory
    
	    $make all
	    $make test
		
		# (Optional)
	    $make runtest
		$make pycaffe

**Unmount SWAP USB**

    $swapoff /dev/sda

**Install pycaffe with Python 3**

    $cd python
    $for req in $(cat requirements.txt); do sudo pip3 install $req; done

**Export PYTHONPATH**

    $echo "export PYTHONPATH=/home/xilinx/caffe/pyth:$PYTHONPATH " >> ~/.bashrc # to be able to call "import caffe" from Python after reboot
    $source ~/.bashrc # Update shell

**Check pycaffe with python3**

    After all this, When python opend and type
    
    $python3
	...
    >>>import caffe

	No error means the pycaffe is work


----------

## Test Caffe ##

There are many examples build out from caffe. You can find them at ~/caffe/build/examples/

I will use the cpp binary (/home/xilinx/caffe/build/examples/cpp_classification/classification.bin) to test caffe with my first small AlexNet mode named dophin_seahorse_model. To get the trained model 

**Train a caffe model**
I'd like to recommend https://github.com/humphd/have-fun-with-machine-learning if you are first time use caffe. If you have a Nvidia GPU, you can refer to my experience about nvidia-docker.  Here is my blog, https://github.com/alexhegit/AlexTryMachineLearning/blob/master/nvidia-docker-run-digits.md



**Run test**

Copy the classification.bin and model files in one directory. And you also need prepare a image(dophin or seahorse) for test.

    xilinx@pynq:~/dophin_seahorse_model$ ls
    classification.bin  deploy.prototxt  image.jpg  labels.txt  mean.binaryproto  snapshot_iter_90.caffemodel
    xilinx@pynq:~/dophin_seahorse_model$ ./classification.bin
    Usage: ./classification.bin deploy.prototxt network.caffemodel mean.binaryproto labels.txt img.jpg

    xilinx@pynq:~/dophin_seahorse_model$ time ./classification.bin deploy.prototxt snapshot_iter_90.caffemodel mean.binaryproto labels.txt image.jpg
    ---------- Prediction for image.jpg ----------
    1.0000 - "dolphin"
    0.0000 - "seahorse"
    
    real	0m6.610s
    user	0m7.959s
    sys	 	0m0.854s
    xilinx@pynq:~/dophin_seahorse_model$



----------

### ISSUES ###
I got these issues and do not get the solution now. Record here and hope we can resolve them in the furture.
If you got the answer, please let me know by create a new issue in the git or sent email to me (ahe@xilinx.com/heye_dev@163.com). Thank you!


**caffe: make runtest failed**

    F1130 04:47:32.171752  9788 test_bbox_util.cpp:279] Check failed: out_bbox.xmax() == 50. (50 vs. 50)
    *** Check failure stack trace: ***
    @   0x7fa4239128  google::LogMessage::Fail()
    @   0x7fa423af98  google::LogMessage::SendToLog()
    @   0x7fa4238c90  google::LogMessage::Flush()
    @   0x7fa423b83c  google::LogMessageFatal::~LogMessageFatal()
    @   0x5572570e38  (unknown)
    @   0x5572778e8c  (unknown)
    @   0x5572772074  (unknown)
    @   0x557277213c  (unknown)
    @   0x557277226c  (unknown)
    @   0x5572772738  (unknown)
    @   0x5572772898  (unknown)
    @   0x5572436d94  (unknown)
    @   0x7fa2e2d6e0  __libc_start_main
    @   0x557243fcec  (unknown)
    Aborted
    Makefile:526: recipe for target 'runtest' failed
    make: *** [runtest] Error 134
  


**pip3 install leveldb failed**

Also reported at https://github.com/Level/leveldown/issues/268 

      $for req in $(cat requirements.txt); do sudo pip3 install $req; done
      ...
      ...
      building 'leveldb' extension
      creating build
      creating build/temp.linux-aarch64-3.6
      creating build/temp.linux-aarch64-3.6/snappy
      creating build/temp.linux-aarch64-3.6/leveldb
      creating build/temp.linux-aarch64-3.6/leveldb/db
      creating build/temp.linux-aarch64-3.6/leveldb/table
      creating build/temp.linux-aarch64-3.6/leveldb/util
      creating build/temp.linux-aarch64-3.6/leveldb/port
      aarch64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fdebug-prefix-map=/build/python3.6-3.6.5=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.6m -c ./snappy/snappy.cc -o build/temp.linux-aarch64-3.6/./snappy/snappy.o -I./leveldb/include -I./leveldb -I./snappy -I. -fno-builtin-memcmp -O2 -fPIC -DNDEBUG -DSNAPPY -pthread -Wall -DOS_LINUX -DLEVELDB_PLATFORM_POSIX
      cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++
      ./snappy/snappy.cc: In member function ‘bool snappy::SnappyIOVecWriter::Append(const char*, size_t)’:
      ./snappy/snappy.cc:1013:33: warning: comparison between signed and unsigned integer expressions [-Wsign-compare]
       if (curr_iov_index_ + 1 >= output_iov_count_) {
       ~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~
      ./snappy/snappy.cc: In member function ‘bool snappy::SnappyIOVecWriter::AppendFromSelf(size_t, size_t)’:
      ./snappy/snappy.cc:1095:35: warning: comparison between signed and unsigned integer expressions [-Wsign-compare]
     if (curr_iov_index_ + 1 >= output_iov_count_) {
     ~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~
      aarch64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fdebug-prefix-map=/build/python3.6-3.6.5=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.6m -c ./snappy/snappy-stubs-internal.cc -o build/temp.linux-aarch64-3.6/./snappy/snappy-stubs-internal.o -I./leveldb/include -I./leveldb -I./snappy -I. -fno-builtin-memcmp -O2 -fPIC -DNDEBUG -DSNAPPY -pthread -Wall -DOS_LINUX -DLEVELDB_PLATFORM_POSIX
      cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++
      aarch64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fdebug-prefix-map=/build/python3.6-3.6.5=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.6m -c ./snappy/snappy-sinksource.cc -o build/temp.linux-aarch64-3.6/./snappy/snappy-sinksource.o -I./leveldb/include -I./leveldb -I./snappy -I. -fno-builtin-memcmp -O2 -fPIC -DNDEBUG -DSNAPPY -pthread -Wall -DOS_LINUX -DLEVELDB_PLATFORM_POSIX
      cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++
      aarch64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fdebug-prefix-map=/build/python3.6-3.6.5=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.6m -c ./snappy/snappy-c.cc -o build/temp.linux-aarch64-3.6/./snappy/snappy-c.o -I./leveldb/include -I./leveldb -I./snappy -I. -fno-builtin-memcmp -O2 -fPIC -DNDEBUG -DSNAPPY -pthread -Wall -DOS_LINUX -DLEVELDB_PLATFORM_POSIX
      cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++
      aarch64-linux-gnu-gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fdebug-prefix-map=/build/python3.6-3.6.5=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/usr/include/python3.6m -c leveldb/db/builder.cc -o build/temp.linux-aarch64-3.6/leveldb/db/builder.o -I./leveldb/include -I./leveldb -I./snappy -I. -fno-builtin-memcmp -O2 -fPIC -DNDEBUG -DSNAPPY -pthread -Wall -DOS_LINUX -DLEVELDB_PLATFORM_POSIX
      cc1plus: warning: command line option ‘-Wstrict-prototypes’ is valid for C/ObjC but not for C++
      In file included from ./leveldb/port/port_posix.h:50:0,
       from ./leveldb/port/port.h:14,
       from ./leveldb/db/filename.h:14,
       from leveldb/db/builder.cc:7:
      ./leveldb/port/atomic_pointer.h:212:2: error: #error Please implement AtomicPointer for this platform.
       #error Please implement AtomicPointer for this platform.
    ^~~~~
      error: command 'aarch64-linux-gnu-gcc' failed with exit status 1
    
      ----------------------------------------
      Failed building wheel for leveldb
      Running setup.py clean for leveldb
    Failed to build leveldb
    Installing collected packages: leveldb
      Running setup.py install for leveldb ... error
    Complete output from command /usr/bin/python3 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-2r5hx3fi/leveldb/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-n8glzehx-record/install-record.txt --single-version-externally-managed --compile:
    running install
    running build
    running build_ext
    building 'leveldb' extension
      