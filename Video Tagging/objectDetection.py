from collections import Counter

import cv2
import imagehash
import requests
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
from PIL import Image

# from videoUtils import getTopKCounter, videoFrames
from videoUtils import videoFrames

setup_logger()

cfg = get_cfg()
cfg.merge_from_file(
    model_zoo.get_config_file(
        "LVIS-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"
    )
)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "LVIS-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"
)
predictor = DefaultPredictor(cfg)


def clusterFrames(frames):
    hashes = [imagehash.average_hash(Image.open(path)) for path in frames]
    marks = [True] * len(hashes)
    for i in range(len(marks)):
        if marks[i]:
            for j in range(len(marks[i + 1 :])):
                if hashes[i] - hashes[j] < 5:
                    marks[j] = False
    return [frames[i] for i in range(len(frames)) if marks[i]]


def getFramesFromVideo(vid, cluster=False):
    frames = videoFrames(vid)
    if cluster:
        frames = clusterFrames(frames)

    return frames


def getObjectsFromFrame(frame):
    cur_image_classes = []
    im = cv2.imread(frame)
    outputs = predictor(im)
    for class_id in outputs["instances"].pred_classes:
        cur_image_classes.append(
            MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[class_id]
        )

    return cur_image_classes


def getDescriptionFromFrame(frame):
    r = requests.post(
        "http://localhost:5000/model/predict",
        files={"image": ("image.png", open(frame, "rb"), "image/png")},
    )
    desc = r.json()["predictions"][0]["caption"]
    return desc

def getFrameDetails(frame):
    classes = getObjectsFromFrame(frame)
    desc = getDescriptionFromFrame(frame)
    return classes, desc
