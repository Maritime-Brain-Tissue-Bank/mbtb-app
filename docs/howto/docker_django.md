## Docker for Django Guidelines
This guide is about building a docker image and run it as a container. please follow these steps:

* First step would be to [install](https://docs.docker.com/install/) docker and view their [guide](https://docs.docker.com/get-started/).
* Create a docker file ['Dockerfile'](../../mbtb_app/resources/apis/user_registration/Dockerfile) in the root directory.
* Build docker image:
    ```shell script
    docker build -t image_name .
    ```
    *Note: `.` represents direcory where Dockerfile is.*
    
* Run container by following command:
    ```shell script
    docker run -it --rm -p 8000:8000 image_name
    ```