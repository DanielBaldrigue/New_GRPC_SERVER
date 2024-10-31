Prompted Pose Estimation Service
===============
Note: This pose estimation works from a top-down view of the object.

This repository contains the code for a prompt based image segmentation and pose estimation pipeline.

The object detection and segmentation is done using lang-segment-anything library. It requires LangSAM to be installed, which is automatically done in the Dockerfile.
 * https://github.com/luca-medeiros/lang-segment-anything

The pose estimation method is a simple plane fitting done using RANSAC. The orientation is estimated by finding the dominant axis using Principle Component Decomposition.

For performance and consitency the model files and other downloaded models is placed in cache.tar.gz. This is done automatically during the docker image building process.

This starts a GRPC based service that remotely expects image files to be sent and it will return the predicted results

# Usage
1- Build the Image
```bash
docker build -t pose_estimation:latest .
```

2- Deploy the container
```bash
docker run --gpus all --net=host -d --name pose_estimation pose_estimation:latest
```