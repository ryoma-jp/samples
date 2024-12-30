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
import time

def time_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@time_function
def load_model(model_path):
    # Load the Hailo8L model
    hef = HEF(model_path)
    return hef

@time_function
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

@time_function
def post_nms_infer(raw_detections):
    boxes = []
    scores = []
    classes = []
    num_detections = 0
    
    input_name = list(raw_detections.keys())[0]
    detections = extract_detections(raw_detections[input_name][0], boxes, scores, classes, num_detections)
    
    return detections

# Dictionary to store fixed colors for each class
CLASS_COLORS = {}

@time_function
def post_process(detections, image, id, width, height, min_score=0.45):
    global CLASS_COLORS
    boxes = np.array(detections['detection_boxes'])[0]
    classes = np.array(detections['detection_classes'])[0].astype(int)
    scores = np.array(detections['detection_scores'])[0]
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    scale_factor = {
        "width": im_width / width,
        "height": im_height / height,
    }

    for idx in range(np.array(detections['num_detections'])[0]):
        if scores[idx] >= min_score:
            if classes[idx] not in CLASS_COLORS:
                # Assign a random color if not already assigned
                CLASS_COLORS[classes[idx]] = tuple(np.random.randint(90, 190, size=3).tolist())
            color = CLASS_COLORS[classes[idx]]
            scaled_box = [x*width if i%2 else x*height for i,x in enumerate(boxes[idx])]
            label = draw_detection(draw, scaled_box , classes[idx], scores[idx]*100.0, color, scale_factor)
    return image

@time_function
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
    draw.rectangle([(xmin * scale_factor["width"], ymin * scale_factor["height"]), (xmax * scale_factor["width"], ymax * scale_factor["height"])], outline=color, width=4)
    text_bbox = draw.textbbox((xmin * scale_factor["width"] + 4, ymin * scale_factor["height"] + 4), label, font=font)
    text_bbox = list(text_bbox)
    text_bbox[0] -= 4
    text_bbox[1] -= 4
    text_bbox[2] += 4
    text_bbox[3] += 4
    draw.rectangle(text_bbox, fill=color)
    draw.text((xmin * scale_factor["width"] + 4, ymin * scale_factor["height"] + 4), label, fill="black", font=font)
    return label

@time_function
def perform_inference_yolox(frame, infer_pipeline, network_group, input_vstream_info):
    # Preprocess the frame
    start_time = time.time()
    input_tensor = cv2.resize(frame, (640, 640))
    print(f"Preprocessing executed in {time.time() - start_time:.4f} seconds")
    
    # Perform inference
    start_time = time.time()
    input_tensor = {input_vstream_info.name: np.array([input_tensor]).astype(np.float32)}
    infer_results = infer_pipeline.infer(input_tensor)
    print(f"Inference executed in {time.time() - start_time:.4f} seconds")
    
    # Post-process the output
    start_time = time.time()
    processed_results = post_nms_infer(infer_results)
    image = Image.fromarray(frame)
    frame = post_process(processed_results, image, 0, 640, 640)
    print(f"Post-processing executed in {time.time() - start_time:.4f} seconds")
    
    return frame  # Return the frame with detections drawn

@time_function
def perform_inference_deeplab_v3(frame, infer_pipeline, network_group, input_vstream_info):
    # Perform inference on the frame using Hailo8L for semantic segmentation with DeeplabV3
    
    # Preprocess the frame
    start_time = time.time()
    frame_height, frame_width = frame.shape[:2]
    input_tensor = cv2.resize(frame, (513, 513))
    input_tensor = np.array([input_tensor]).astype(np.float32)
    print(f"Preprocessing executed in {time.time() - start_time:.4f} seconds")
    
    # Perform inference
    start_time = time.time()
    input_tensor = {input_vstream_info.name: np.array([input_tensor]).astype(np.float32)}
    infer_results = infer_pipeline.infer(input_tensor)
    print(f"Inference executed in {time.time() - start_time:.4f} seconds")
    
    # Post-process the output
    start_time = time.time()
    input_name = list(infer_results.keys())[0]
    output_tensor = infer_results[input_name][0]
    output_tensor = np.argmax(output_tensor, axis=-1)
    
    # Create a mask
    input_frame = Image.fromarray(frame).resize((513, 513))
    mask = np.zeros_like(np.array(input_frame))
    for i in range(21):
        if int(i) not in CLASS_COLORS:
            if int(i) == 0:
                CLASS_COLORS[int(i)] = (0, 0, 0)
            else:
                CLASS_COLORS[int(i)] = tuple(np.random.randint(21, 255, size=3).tolist())
        mask[output_tensor == i] = np.array(CLASS_COLORS[int(i)])
    
    frame = Image.blend(input_frame, Image.fromarray(mask), alpha=0.5).resize((frame_width, frame_height))
    print(f"Post-processing executed in {time.time() - start_time:.4f} seconds")

    return frame  # Return the frame with detections drawn

# Dictionary to map model names to their respective inference functions
MODEL_INFERENCE_FUNCTIONS = {
    "yolox_l_leaky.hef": perform_inference_yolox,
    "yolox_s_leaky.hef": perform_inference_yolox,
    "deeplab_v3_mobilenet_v2.hef": perform_inference_deeplab_v3,
}

@time_function
def perform_inference(model_name, frame, infer_pipeline, network_group, input_vstream_info):
    # Select the appropriate inference function based on the model name
    inference_function = MODEL_INFERENCE_FUNCTIONS.get(model_name, perform_inference_yolox)
    
    # Perform inference using the selected function
    return inference_function(frame, infer_pipeline, network_group, input_vstream_info)

def main():
    parser = argparse.ArgumentParser(description="Camera streaming with inference")
    parser.add_argument('--hef', type=str, required=True, help='Path to the Hailo8L model file')
    args = parser.parse_args()
    
    camera = Picamera2()
    camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
    camera.start()
    
    hef = load_model(args.hef)  # Load the model with the provided path
    hef_name = args.hef.split("/")[-1]
    
    # Configure network groups
    start_time = time.time()
    params = VDevice.create_params()
    target = VDevice(params)
    configure_params = ConfigureParams.create_from_hef(hef=hef, interface=HailoStreamInterface.PCIe)
    network_groups = target.configure(hef, configure_params)
    network_group = network_groups[0]
    network_group_params = network_group.create_params()
    print(f"Network configuration executed in {time.time() - start_time:.4f} seconds")

    start_time = time.time()
    input_vstreams_params = InputVStreamParams.make(network_group, quantized=False,
                                                    format_type=FormatType.FLOAT32)
    output_vstreams_params = OutputVStreamParams.make(network_group, quantized=True,
                                                    format_type=FormatType.FLOAT32)
    input_vstream_info = hef.get_input_vstream_infos()[0]
    output_vstream_info = hef.get_output_vstream_infos()[0]
    print(f"Stream parameters setup executed in {time.time() - start_time:.4f} seconds")
    
    with InferVStreams(network_group, input_vstreams_params, output_vstreams_params) as infer_pipeline:
        with network_group.activate(network_group_params):
            root = tk.Tk()
            root.title("Camera Streaming")
            label = tk.Label(root)
            label.pack()
            
            update_camera(hef_name, camera, label, infer_pipeline, network_group, input_vstream_info)
            root.mainloop()

@time_function
def update_camera(model_name, camera, label, infer_pipeline, network_group, input_vstream_info):
    frame = camera.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    
    frame = perform_inference(model_name, frame, infer_pipeline, network_group, input_vstream_info)  # Perform inference
    
    frame = ImageTk.PhotoImage(frame)
    label.config(image=frame)
    label.image = frame
    label.after(10, lambda: update_camera(model_name, camera, label, infer_pipeline, network_group, input_vstream_info))
    
if __name__ == "__main__":
    main()
