# CZI Images

CZI Images is a rest api in C++, through which one can read CZI images, extract subblocks, region of interest (ROI), save it as png. 
This api uses following libraries: [libCZI](https://github.com/zeiss-microscopy/libCZI), [cpprestsdk](https://github.com/microsoft/cpprestsdk).

## How to Build (Mac OS)

1. Install Homebrew 
    ```shell script
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```
   
2. Install git, cmake, boost, zlib, cpprestsdk openssl with brew
    ```shell script
    $ brew install cmake git openssl boost zlib cpprestsdk
    ```

3. Inside the root directory of this api, excute following commands:
    ```shell script
    $ mkdir build
    $ cd build
    $ cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug ..
    ```
   
4. Finally type the command:
    ```shell script
    $ make -j 8
    ```
