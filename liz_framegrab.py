# Imports
import ffmpeg
import os
import random
from dotenv import load_dotenv


# Load parameters
load_dotenv()
path = os.getenv('LIZ_PATH')
startTime = 36.5
endTime = 5094.5


# Frame grab function
def lizGetScreencap():
    # Delete old frame file(s)
    for file in os.scandir("./liz_frames/jpg"):
        os.remove(file.path)
    for file in os.scandir("./liz_frames/png"):
        os.remove(file.path)

    # Get video file information
    probe = ffmpeg.probe(path)
    width = probe['streams'][0]['width']

    # Get random timestamp
    time = round(random.uniform(startTime, endTime), 2)
    print("timestamp: ",time)

    # Grab and save frame
    ffmpeg.input(path, ss=time).filter('scale', width, -1).output("./liz_frames/png/Liz_" + str(time) + ".png", vframes=1, loglevel="quiet").run()
    ffmpeg.input(path, ss=time).filter('scale', width, -1).output("./liz_frames/jpg/Liz_" + str(time) + ".jpg", vframes=1, loglevel="quiet").run()

    # Return caption
    return str(round(time))


# Function call
# lizGetScreencap()