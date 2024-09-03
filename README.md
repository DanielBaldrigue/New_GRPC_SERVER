Prompted Pose Estimation Service
===============
Note: This pose estimation works from a top-down view of the object.

This repository contains the code for a prompt based image segmentation and pose estimation pipeline.

The pose detection and segmentation is done using lang-segment-anything library. It requires LangSAM to be installed, which is automatically done in the Dockerfile.
 * https://github.com/luca-medeiros/lang-segment-anything

The pose estimation method is a simple plane fitting done using RANSAC. The orientation is estimated by finding the dominant axis using Principle Component Decomposition.

For performance and consitency the model files and other downloaded models is placed in cache.tar.gz, unpack this tarball to cache/ before trying to build the docker image.

[Download Cache file](https://drive.google.com/file/d/1NM0yjs9t3NHQwM4PWIqYWqlnIS23OM-3/view?usp=drive_link)

```
tar xvzf cache.tar.gz
```

This starts a GRPC based service that remotely expects image files to be sent and it will return the predicted results