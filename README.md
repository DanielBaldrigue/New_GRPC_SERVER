<<<<<<< HEAD
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
=======
# New_GRPC_SERVER

This repository contains a gRPC server implementation designed to handle image processing tasks using machine learning models. The server facilitates efficient communication between clients and the image processing backend, enabling seamless integration into various applications.

## Features

- **gRPC Protocol**: Leverages the high-performance gRPC framework for efficient client-server communication.
- **Image Processing Pipelines**: Implements customizable pipelines for processing images using machine learning models.
- **Modular Design**: Structured to allow easy integration of additional functionalities or models.

## Repository Structure

- `LangSAM_image_pipeline.py`: Defines the image processing pipeline utilizing the LangSAM model.
- `Load_Default.py`: Contains default settings and configurations for the server.
- `ML_Detector.py`: Implements machine learning-based detection algorithms.
- `pipeline.proto`: Protocol buffer definitions outlining the gRPC service and messages.
- `pipeline_pb2.py`, `pipeline_pb2.pyi`, `pipeline_pb2_grpc.py`: Generated files from the `pipeline.proto` definition, facilitating gRPC communication.

## Getting Started

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system.
- **gRPC Tools**: Install the gRPC tools for Python:
  ```bash
  pip install grpcio grpcio-tools

Installation
1 - Clone the Repository:
git clone https://github.com/DanielBaldrigue/New_GRPC_SERVER.git
2 - Navigate to the Project Directory:
cd New_GRPC_SERVER
3 - Install Required Dependencies:
pip install -r requirements.txt

Running the Server
To start the gRPC server, execute:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pipeline.proto
python server.py

Replace server.py with the actual server implementation file if it differs.

Testing the Server
You can test the server using a gRPC client. Ensure that the client adheres to the service definitions outlined in pipeline.proto.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

License
This project is licensed under the MIT License. See the LICENSE file for details.
>>>>>>> 0cc6701f51762475eb97f4f194ded538d56ef1cd
