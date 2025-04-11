from typing import Optional
import grpc
from google.protobuf.internal import containers as _containers
import pipeline_pb2, pipeline_pb2_grpc
import rclpy
from rclpy.node import Node


import numpy as np
import cv2 as cv

class MLDetector:
    def __init__(self, endpoint, api_key="test"):
        self.endpoint = endpoint
        self.api_key = api_key

    def check_connection(self):
        with grpc.insecure_channel(self.endpoint) as channel:
            stub = pipeline_pb2_grpc.ImageModelPipelineStub(channel)
            response = stub.Ping(pipeline_pb2.PingRequest(seq=1))
            if response.seq != 1:
                raise Exception("Cannot connect to the detection server")

    def detect(self, node:Node, rgb_image, prompt="object", box_threshold=0.25, text_threshold=0.25)->Optional[np.ndarray]:
        """
        Do detection of rgb_image using a prompt

        Parameters:
            rgb_image: An OpenCV image in RGB color space.
            prompt: What to search for (may be None, then default value is used)

        Returns:
            Masks of identified objects or None if no object could be found
        """
        node.get_logger().info('Start detection')
        attempts = 0
        while attempts < 5:

            success, rgb_rawdata = cv.imencode(".jpg", rgb_image, [cv.IMWRITE_JPEG_QUALITY, 100])
            node.get_logger().info('Received image')
            assert success, "Could not encode image"

            predictions = self.detect_raw(prompt, pipeline_pb2.Image(image_format="jpg", image_data=bytes(rgb_rawdata)), box_threshold, text_threshold)
            node.get_logger().info('Go results')
            
            masks = []
            scores = []
            
            if len(predictions.masks) > 0:
                for mask in predictions.masks:
                    
                    scores.append(mask.score)
                    masks.append(np.unpackbits(np.frombuffer(mask.packedbits, dtype=np.uint8), count=mask.w*mask.h).reshape(mask.h, mask.w))
                return masks, predictions.regions, scores, predictions.label
            attempts += 1
        
        node.get_logger().info('Got no results')
        return None
    
    def detect_raw(self, prompt: str, img: pipeline_pb2.Image, box_threshold: float, text_threshold: float)->pipeline_pb2.ObjectDetectionReply:
        """
        Send image and prompt to image pipeline, internal method

        Parameters:
            prompt: what to search for
            img: encoded image for the service

        Returns:
            Service reply
        """
        with grpc.insecure_channel(self.endpoint) as channel:
            stub = pipeline_pb2_grpc.ImageModelPipelineStub(channel)
            return stub.PromptObjectDetection(pipeline_pb2.PromptObjectDetectionRequest(api_key=self.api_key, prompt=prompt, image=img, box_threshold=box_threshold, text_threshold=text_threshold))
        