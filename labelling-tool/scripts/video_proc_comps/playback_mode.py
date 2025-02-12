from enum import Enum

class PlaybackMode(Enum):
    STOPPED = 0
    PLAYING = 1
    REWINDING = 2
    FORWARDING = 3
