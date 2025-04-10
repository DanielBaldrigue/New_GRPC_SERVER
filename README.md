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
