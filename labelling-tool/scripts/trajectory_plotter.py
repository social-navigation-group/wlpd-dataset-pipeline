import cv2
import numpy as np

class TrajectoryPlotter:
    @staticmethod
    def plot_trajectories(video_path, save_path, traj_file):
        data = np.load(traj_file, allow_pickle=True)
        trajectories = data['trajectories']
        traj_starts = data['traj_starts']

        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'XVID'), frame_rate, (frame_width, frame_height))

        colors = np.array([
            [255, 255, 255], [0, 255, 255], [255, 0, 255],
            [255, 255, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]
        ], dtype=np.uint8)
        num_colors = colors.shape[0]

        ped_set = [False] * len(trajectories)
        mask_set = [np.zeros((frame_height, frame_width, 3), dtype=np.uint8) for _ in range(len(trajectories))]
        curr_pt_set = np.zeros((len(trajectories), 2), dtype=int)

        vid_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            for i, traj in enumerate(trajectories):
                if traj_starts[i] <= vid_idx < traj_starts[i] + len(traj):
                    ped_set[i] = True
                    pt = np.round(traj[vid_idx - traj_starts[i]]).astype(int)

                    ws = 3
                    window_r = slice(max(pt[1] - ws, 0), min(pt[1] + ws, frame_height))
                    window_c = slice(max(pt[0] - ws, 0), min(pt[0] + ws, frame_width))
                    mask_set[i][window_r, window_c] = colors[i % num_colors]

                    curr_pt_set[i] = pt
                else:
                    ped_set[i] = False

            for i, active in enumerate(ped_set):
                if active:
                    color_mask = mask_set[i]
                    frame = cv2.addWeighted(frame, 1, color_mask, 0.5, 0)
                    cv2.putText(frame, str(i + 1), tuple(curr_pt_set[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            out.write(frame)
            vid_idx += 1

        cap.release()
        out.release()