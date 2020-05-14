# CZI Images

CZI Images is a rest api in C++ 14, through which one can read CZI images, extract subblocks, region of interest (ROI), save it as png. 
This api uses following libraries: [libCZI](https://github.com/zeiss-microscopy/libCZI), [cpprestsdk](https://github.com/microsoft/cpprestsdk).

## How to Build (Mac OS)

1. Install Homebrew 
    ```shell script
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```
   
2. Install git, cmake, boost, zlib, cpprestsdk openssl, mysql, mysql-connector-c++ with brew
    ```shell script
    $ brew install cmake git openssl boost zlib cpprestsdk mysql mysql-connector-c++
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

## Rest Endpoints

```shell script
base url: 127.0.0.1:7000
```

1. Base request
    ```shell script
    url: 127.0.0.1:7000/
   
   response:
   {
     "message": "Welcome to the image api"
   }
    ```
   
2. Get tissue meta data
    ```shell script
    url: {base}/tissue_meta_data/{tissueId},
    headers: {
         'Authorization': 'Token ' + {token},
    }
   
    response:
    {
      "region_1": [
        {
          "file_name": "file_name_1",
          "stain_name": "stain_1"
        },
        {
         "file_name": "file_name_2",
         "stain_name": "stain_2"
        }
      ],
      "region_2": [
        {
          "file_name": "file_name_3",
          "stain_name": "stain_3"
        }
      ]
    }
    ```
   
3. For original tissue image
    ```shell script
    url: {base}/czi_image/,
    headers: {
         'Authorization': 'Token ' + {token},
         'Content-Type': application/json
    },
   json: {
        "filename": "filename",
        "has_meta_data": false,
    }
   
   response:
   > png image
   ```
   
4. For extracting ROI
    ```shell script
    url: {base}/czi_image/,
    headers: {
         'Authorization': 'Token ' + {token},
         'Content-Type': application/json
    },
    json: {
        "filename": "filename",
        "has_meta_data": true,
       	"meta_data":{
       		"w": int value,
       		"h": int value,
       		"x": int value,
       		"y": int value
       	}
    }
       
    response:
    > png image
     ```