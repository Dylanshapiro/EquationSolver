from Utilities.Image import EqSolImage
import numpy as np
from Utilities.box import Box
import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class SymbolDetector:
    def __init__(self, modelPath, labelsPath, numClasses):
        PATH_TO_CKPT = os.path.join(modelPath , 'frozen_inference_graph.pb')
        self.numClasses = numClasses
        self.label_map = label_map_util.load_labelmap(labelsPath)
        self.categories = label_map_util.convert_label_map_to_categories(
            self.label_map, max_num_classes=self.numClasses, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.sess = tf.Session(graph=self.detection_graph)

        categories = label_map_util.convert_label_map_to_categories(
            self.label_map, max_num_classes=numClasses, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    '''
    Boxes and labels symbols
    
    Author: Matthew Schofield
    Version: 4/29/2020
    '''
    def box(self, image:EqSolImage):
        size = image.getSize()
        height = size["height"]
        width = size["width"]
        image = image.getPixels()

        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        image_expanded = np.expand_dims(image, axis=0)
        (boxes, scores, classes, num) = self.sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})
        # Draw the results of the detection (aka 'visualize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=4,
            min_score_thresh=0.70)


        outBoxes = []
        for box, score, class_ in zip(np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes).astype(np.int32)):
            if score < .7:
                break
            objClass = self.category_index[class_]['name']
            boxObj = Box([box[1] * width, box[0] * width, box[3] * height, box[2] * height], method="fixed", label=objClass)
            outBoxes.append(boxObj)
        return outBoxes, image
