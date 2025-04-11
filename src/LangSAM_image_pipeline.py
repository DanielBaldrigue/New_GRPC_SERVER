import math
import grpc
import pipeline_pb2
import pipeline_pb2_grpc
from PIL import Image
from lang_sam import LangSAM
from io import BytesIO
import numpy as np
from concurrent import futures
import logging
import threading
import os

from pose_estimator import POSE, estimate_pose
import torch

class LangSAM_Service(pipeline_pb2_grpc.ImageModelPipelineServicer):
    def __init__(self, api_keys, sam_model="vit_l"):
        self.model = LangSAM(sam_type=sam_model)
        self.api_keys = api_keys
        self.lock = threading.Lock()
        pass

    def Ping(self, request: pipeline_pb2.PingRequest, context)->pipeline_pb2.PingReply:
        return pipeline_pb2.PingReply(seq=request.seq)

    def PromptObjectDetection(self, request: pipeline_pb2.PromptObjectDetectionRequest, context)->pipeline_pb2.ObjectDetectionReply:
        if request.api_key not in self.api_keys:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Invalid api key")
            return pipeline_pb2.ObjectDetectionReply()

        rawdata = BytesIO(request.image.image_data)
        prompt = request.prompt if request.HasField("prompt") else ""
        box_threshold = request.box_threshold if request.HasField("box_threshold") else 0.25
        text_threshold = request.text_threshold if request.HasField("text_threshold") else 0.25
        with self.lock:
            img = Image.open(rawdata)
            
            masks, boxes, label_class, scores = self.model.predict(images_pil = img, texts_prompt = prompt, box_threshold = box_threshold, text_threshold = text_threshold)

            masks_pb = []
            regions_pb = []
            for i in range(len(masks)):
                cpu_mask = masks[i].cpu().numpy()
                mask = pipeline_pb2.Mask(w = cpu_mask.shape[1], h=cpu_mask.shape[0], score=scores[i], packedbits=np.packbits(cpu_mask.flatten()).tobytes())
                masks_pb.append(mask)

                cpu_box = boxes[i].cpu()
                box = pipeline_pb2.Region(x=round(cpu_box[0].item()),y=round(cpu_box[1].item()),w=round((cpu_box[2]-cpu_box[0]).item()),h=round((cpu_box[3]-cpu_box[1]).item()))
                regions_pb.append(box)
                
            return pipeline_pb2.ObjectDetectionReply(masks=masks_pb, regions=regions_pb, label=[prompt]*len(masks))

def serve():
    port = os.environ.get("GRPC_PORT", "50051")
    api_keys = os.environ.get("API_KEYS", "test")
    sam_model = os.environ.get("SAM_MODEL", "vit_l")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = LangSAM_Service(api_keys=set(api_keys.split(",")), sam_model=sam_model)
    pipeline_pb2_grpc.add_ImageModelPipelineServicer_to_server(service, server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()