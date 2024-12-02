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

2- Create and deploy the container
```bash
docker run --gpus all --net=host -d --name pose_estimation pose_estimation:latest
```

3- The container can be started/stopped on demand using
```bash
docker start pose_estimation
```
or
```bash
docker stop pose_estimation
```

# API Implementation
Copy client.py, pipeline_pb2_grpc.py, pipeline_pb2.py and pipeline_pb2.pyi into your client side code.
```python
    from client import MLDetector

    detector = MLDetector("localhost:50051")  # change localhost with ip_address if running the container on separate machine

    # For segmentation
    masks, boxes, scores, labels = detector.detect(rgb_image, text_prompt)

    # For pose-estimation
    pose, masks, boxes, scores, labels = detector.detect_pose(
        rgb_image,
        depth_image,
        camera_intrinsics, # 3x3 camera matrix
        text_prompt,
        Confidence_Threshold)
```