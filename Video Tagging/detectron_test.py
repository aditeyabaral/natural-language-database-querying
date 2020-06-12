import cv2
import detectron2
import numpy as np
import torch
import torchvision
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer

setup_logger()


print(torch.__version__, torch.cuda.is_available())


im = cv2.imread("./input.jpg")

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

# For panoptic segmentation models
# panoptic_seg, segments_info = predictor(im)["panoptic_seg"]
# for obj in segments_info:
#   if obj["isthing"]:
#     print(MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[obj["category_id"]])
#   else:
#     print(MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).stuff_classes[obj["category_id"]])
# print(len(MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes))
# v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
# v = v.draw_panoptic_seg_predictions(panoptic_seg.to("cpu"), segments_info)

# For instance segmentation models
outputs = predictor(im)
print(MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes)
v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2.imshow("vis", v.get_image()[:, :, ::-1])
while True:
    ch = cv2.waitKey(0)
    if ch == ord("q"):
        cv2.destroyAllWindows()
        break

