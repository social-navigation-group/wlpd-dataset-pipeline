import cv2

def anonymize_region(frame, x1, y1, x2, y2, object_id):
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    label = f"ID: {object_id}" if object_id is not None else "ID: N/A"
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    region = frame[y1:y2, x1:x2]
    region = cv2.blur(region, (40, 40))
    frame[y1:y2, x1:x2] = region
    
    return frame

def main(video_path, output_path, bbox_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video {video_path}.")
        return
    
    # GET VIDEO PROPERTIES
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    bbox_values = {}
    try:
        with open(bbox_path, 'r') as bbox_file:
            for line in bbox_file:
                frm_id, x_min, y_min, x_max, y_max, class_id, conf, obj_id = line.strip().split(', ')

                # CONVERTING
                frame_id = int(frm_id)
                x1, y1, x2, y2 = map(int, [x_min, y_min, x_max, y_max])
                confidence = float(conf)
                object_id = int(obj_id) if obj_id != 'N/A' else None

                if frame_id not in bbox_values:
                    bbox_values[frame_id] = []
                bbox_values[frame_id].append((x1, y1, x2, y2, class_id, confidence, object_id))
    except FileNotFoundError:
        print(f"ERROR: The file {bbox_path} does not exist.")
        return
    except IOError as io_err:
        print(f"ERROR: Cannot read file {bbox_path}. DETAILS: {io_err}")
        return
    except Exception as e:
        print(f"ERROR: {e}")
        return

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx in bbox_values:
            print(f"In frame {frame_idx}\n")

            for bbox in bbox_values[frame_idx]:
                x1, y1, x2, y2, class_id, confidence, object_id = bbox

                bbox_height = y2 - y1
                crop_height = int(bbox_height * 0.2)
                crop_height = max(crop_height, 25) # 25 is the min crop height
                y2 = y1 + crop_height

                frame = anonymize_region(frame, x1, y1, x2, y2, object_id)
        
        output.write(frame)
        frame_idx += 1
    print(f"Finished writing bounding boxes in the video")
    
    # RELEASE RESOURCES
    cap.release()
    output.release()

if __name__ == "__main__":
    bbox_path = "./btrack_bboxes.txt"
    video_path = "path/file.mp4"
    output_path = "./tracked_output.mp4"

    main(video_path, output_path, bbox_path)
