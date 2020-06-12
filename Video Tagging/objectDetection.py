import cv2
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
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

frames = videoFrames("sample15.mp4")
classes = set()
for image in frames:
    print(image)
    im = cv2.imread(image)
    print(im)
    outputs = predictor(im)
    for class_id in outputs["instances"].pred_classes:
        classes.add(MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[class_id])

print(classes)

