# Anonymization (Current)

## Overview
The anonymization process is straightforward, though the scripts can be optimized further (including the method). For now, we’ll proceed with the current approach, with plans to make it more robust and reliable in the future. What do you need to do:

- Obtain the video you want to anonymize.
- Download the required model.
- Input the correct file paths into each script.
- Run the first script (yolo_tracking.py) to initiate tracking - get bbox coordinates.
- Run the second script (write_bbox.py) to complete the anonymization.
- Once completed, you’ll have the final anonymized video.