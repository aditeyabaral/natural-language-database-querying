import cv2
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
from videoUtils import videoFrames, getTopKCounter
from collections import Counter

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

def importantFrames(vid):
    frames = videoFrames(vid)
    classes = []
    image_classes = []
    for image in frames:
        cur_image_classes = []
        im = cv2.imread(image)
        outputs = predictor(im)
        for class_id in outputs["instances"].pred_classes:
            cur_image_classes.append(
                MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[class_id]
            )
            classes.append(
                MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[class_id]
            )
        image_classes.append(cur_image_classes)

    imp_classes = getTopKCounter([classes], 5)
    imp_frames = []
    for frame, image_tags in zip(frames, image_classes):
        if set(image_tags).intersection(set(imp_classes)):
            imp_frames.append(frame)

    return imp_classes, imp_frames
