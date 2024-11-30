"""
Sample code to stream camera feed using OpenCV
"""
import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from picamera2 import Picamera2
from hailo_platform import (HEF, ConfigureParams, FormatType, HailoSchedulingAlgorithm, HailoStreamInterface,
                            InferVStreams, InputVStreamParams, InputVStreams, OutputVStreamParams, OutputVStreams,
                            VDevice)
import argparse
import numpy as np

def load_model(model_path):
    # Load the Hailo8L model
    hef = HEF(model_path)
    return hef

def extract_detections(input, boxes, scores, classes, num_detections, threshold=0.5):   
    for i, detection in enumerate(input):
        if len(detection) == 0:
            continue
        for j in range(len(detection)):
            bbox = np.array(detection)[j][:4]
            score = np.array(detection)[j][4]
            if score < threshold:
                continue
            else:
                boxes.append(bbox)
                scores.append(score)
                classes.append(i)
                num_detections = num_detections + 1
    return {'detection_boxes': [boxes], 
              'detection_classes': [classes], 
             'detection_scores': [scores],
             'num_detections': [num_detections]}

def post_nms_infer(raw_detections, input_name):
    boxes = []
    scores = []
    classes = []
    num_detections = 0
    
    detections = extract_detections(raw_detections[input_name][0], boxes, scores, classes, num_detections)
    
    return detections

def post_process(detections, image, id, width, height, min_score=0.45, scale_factor=1):
    COLORS = np.random.randint(90, 190, size=(100, 3), dtype=np.uint8)
    boxes = np.array(detections['detection_boxes'])[0]
    classes = np.array(detections['detection_classes'])[0].astype(int)
    scores = np.array(detections['detection_scores'])[0]
    draw = ImageDraw.Draw(image)

    for idx in range(np.array(detections['num_detections'])[0]):
        if scores[idx] >= min_score:
            color = tuple(int(c) for c in COLORS[classes[idx]])
            scaled_box = [x*width if i%2 else x*height for i,x in enumerate(boxes[idx])]
            label = draw_detection(draw, scaled_box , classes[idx], scores[idx]*100.0, color, scale_factor)
    return image

def draw_detection(draw, d, c, s, color, scale_factor):
    """Draw box and label for 1 detection."""
    # same as coco.txt
    class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
               'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
               'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
               'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
               'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    label = class_names[c] + ": " + "{:.2f}".format(s) + '%'
    ymin, xmin, ymax, xmax = d
    font = ImageFont.truetype("LiberationSans-Regular.ttf", size=18)
    draw.rectangle([(xmin * scale_factor, ymin * scale_factor), (xmax * scale_factor, ymax * scale_factor)], outline=color, width=4)
    text_bbox = draw.textbbox((xmin * scale_factor + 4, ymin * scale_factor + 4), label, font=font)
    text_bbox = list(text_bbox)
    text_bbox[0] -= 4
    text_bbox[1] -= 4
    text_bbox[2] += 4
    text_bbox[3] += 4
    draw.rectangle(text_bbox, fill=color)
    draw.text((xmin * scale_factor + 4, ymin * scale_factor + 4), label, fill="black", font=font)
    return label

def perform_inference(hef, frame):
    # Perform inference on the frame using Hailo8L
    # This implementation is sample code for yolox_s_leaky_h8l_rpi.hef
    
    # Preprocess the frame
    input_tensor = cv2.resize(frame, (640, 640))
    
    # Configure network groups
    params = VDevice.create_params()
    target = VDevice(params)
    configure_params = ConfigureParams.create_from_hef(hef=hef, interface=HailoStreamInterface.PCIe)
    network_groups = target.configure(hef, configure_params)
    network_group = network_groups[0]
    network_group_params = network_group.create_params()

    input_vstreams_params = InputVStreamParams.make(network_group, quantized=False,
                                                    format_type=FormatType.FLOAT32)
    output_vstreams_params = OutputVStreamParams.make(network_group, quantized=True,
                                                    format_type=FormatType.FLOAT32)

    input_vstream_info = hef.get_input_vstream_infos()[0]
    #print("input shape - ", input_vstream_info.shape)

    output_vstream_info = hef.get_output_vstream_infos()[0]
    #print("output shape - ", output_vstream_info.shape)
    
    # Perform inference
    input_tensor = {input_vstream_info.name: np.array([input_tensor]).astype(np.float32)}
    with InferVStreams(network_group, input_vstreams_params, output_vstreams_params) as infer_pipeline:
        with network_group.activate(network_group_params):
            infer_results = infer_pipeline.infer(input_tensor)
    
    # Post-process the output
    # This is a placeholder for post-processing code
    #print(infer_results)
    processed_results = post_nms_infer(infer_results, "yolox_l_leaky/yolox_nms_postprocess")
    image = Image.fromarray(frame)
    frame = post_process(processed_results, image, 0, 640, 640)
    
    return frame  # Return the frame with detections drawn

def main():
    parser = argparse.ArgumentParser(description="Camera streaming with inference")
    parser.add_argument('--hef', type=str, required=True, help='Path to the Hailo8L model file')
    args = parser.parse_args()
    
    camera = Picamera2()
    camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
    camera.start()
    
    hef = load_model(args.hef)  # Load the model with the provided path
    
    root = tk.Tk()
    root.title("Camera Streaming")
    label = tk.Label(root)
    label.pack()
    
    update_camera(camera, label, hef)
    root.mainloop()
    
def update_camera(camera, label, hef):
    frame = camera.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    frame = perform_inference(hef, frame)  # Perform inference
    
    frame = ImageTk.PhotoImage(frame)
    label.config(image=frame)
    label.image = frame
    label.after(10, lambda: update_camera(camera, label, hef))
    
if __name__ == "__main__":
    main()
