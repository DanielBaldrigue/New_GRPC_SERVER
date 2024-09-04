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

class LangSAM_Service(pipeline_pb2_grpc.ImageModelPipelineServicer):
    def __init__(self, api_keys):
        self.model = LangSAM(sam_type="vit_l")
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
        with self.lock:
            img = Image.open(rawdata)
            
            masks, boxes, phrases, logits = self.model.predict(img, request.prompt)

            masks_pb = []
            regions_pb = []
            for i in range(len(masks)):
                cpu_mask = masks[i].cpu().numpy()
                mask = pipeline_pb2.Mask(w = cpu_mask.shape[1], h=cpu_mask.shape[0], score=logits[i], packedbits=np.packbits(cpu_mask.flatten()).tobytes())
                masks_pb.append(mask)

                cpu_box = boxes[i].cpu()
                box = pipeline_pb2.Region(x=round(cpu_box[0].item()),y=round(cpu_box[1].item()),w=round((cpu_box[2]-cpu_box[0]).item()),h=round((cpu_box[3]-cpu_box[1]).item()))
                regions_pb.append(box)
                
            return pipeline_pb2.ObjectDetectionReply(masks=masks_pb, regions=regions_pb, label=[request.prompt]*len(masks))

    def PoseDetection(self, request: pipeline_pb2.PoseDetectionRequest, context)->pipeline_pb2.PoseDetectionReply:
        if request.api_key not in self.api_keys:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Invalid api key")
            return pipeline_pb2.PoseDetectionReply()

        rgb_rawdata = BytesIO(request.rgb.image_data)
        depth_rawdata = BytesIO(request.depth.image_data)
        intrinsics = np.array(request.intrinsics).reshape(3,3)
        with self.lock:
            rgb = Image.open(rgb_rawdata)
            depth = Image.open(depth_rawdata)
            
            masks, boxes, phrases, logits = self.model.predict(rgb, request.prompt, box_threshold=request.box_threshold)

            masks_pb = []
            regions_pb = []
            poses_pb = []
            for i in range(len(masks)):
                cpu_mask = masks[i].cpu().numpy()
                mask = pipeline_pb2.Mask(w = cpu_mask.shape[1], h=cpu_mask.shape[0], score=logits[i], packedbits=np.packbits(cpu_mask.flatten()).tobytes())
                masks_pb.append(mask)

                cpu_box = boxes[i].cpu()
                box = pipeline_pb2.Region(x=round(cpu_box[0].item()),y=round(cpu_box[1].item()),w=round((cpu_box[2]-cpu_box[0]).item()),h=round((cpu_box[3]-cpu_box[1]).item()))
                regions_pb.append(box)

                pose = estimate_pose(cpu_mask, depth, intrinsics)
                pose_pb = [pose.position[0], pose.position[1], pose.position[2], pose.euler[0], pose.euler[1], pose.euler[2]]
                poses_pb.append(pose_pb)
                
            return pipeline_pb2.PoseDetectionReply(masks=masks_pb, regions=regions_pb, label=[request.prompt]*len(masks), pose=poses_pb)


def serve():
    port = os.environ.get("GRPC_PORT", "50051")
    api_keys = os.environ.get("API_KEYS", "test")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pipeline_pb2_grpc.add_ImageModelPipelineServicer_to_server(LangSAM_Service(api_keys=set(api_keys.split(","))), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()