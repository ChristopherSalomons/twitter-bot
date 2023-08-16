# Imports
import os
import ffmpeg
import random
from dotenv import load_dotenv


# Load parameters
load_dotenv()
path = os.getenv('HYOUKA_PATH')
fileNames = [
    "Hyouka - 11.5.mkv",
    "Hyouka - 01.mkv",
    "Hyouka - 02.mkv",
    "Hyouka - 03.mkv",
    "Hyouka - 04.mkv",
    "Hyouka - 05.mkv",
    "Hyouka - 06.mkv",
    "Hyouka - 07.mkv",
    "Hyouka - 08.mkv",
    "Hyouka - 09.mkv",
    "Hyouka - 10.mkv",
    "Hyouka - 11.mkv",
    "Hyouka - 12.mkv",
    "Hyouka - 13.mkv",
    "Hyouka - 14.mkv",
    "Hyouka - 15.mkv",
    "Hyouka - 16.mkv",
    "Hyouka - 17.mkv",
    "Hyouka - 18.mkv",
    "Hyouka - 19.mkv",
    "Hyouka - 20.mkv",
    "Hyouka - 21.mkv",
    "Hyouka - 22.mkv"
]


# Frame grab function
def hyoukaGetScreencap():
    global path

    # Delete old frame file(s)
    for file in os.scandir("./hyouka_frames/png"):
        os.remove(file.path)
    for file in os.scandir("./hyouka_frames/jpg"):
        os.remove(file.path)

    # Select random episode
    episode = random.randint(0,22)
    path += "/" + fileNames[episode]
    episodeStr = ""
    if episode == 0:
        episodeStr = "Episode 11.5"
    else:
        episodeStr = "Episode " + str(episode)

    # Get video file information
    probe = ffmpeg.probe(path, show_chapters=None)
    width = probe["streams"][0]["width"]
    episodeEnd = float(probe["format"]["duration"])
    opStart = float(probe["chapters"][1]["start_time"])
    opEnd = float(probe["chapters"][1]["end_time"])
    edStart = float(probe["chapters"][4]["start_time"])
    edEnd = float(probe["chapters"][4]["end_time"])

    # Get random timestamp
    while True:
        time = round(random.uniform(0, episodeEnd), 2)
        # Check if random timestamp is during intro
        if time > opStart and time < opEnd:
            if episode == 1 or episode == 12:
                # Calculate equivalent timestamp for creditless video file
                print("Calculating new timestamp for creditless op.")
                time = round(time - opStart, 2)
                if episode == 1:
                    path = os.getenv('HYOUKA_PATH') + "/Hyouka - NCOP1.mkv"
                    episodeStr = "OP1"
                else:
                    path = os.getenv('HYOUKA_PATH') + "/Hyouka - NCOP2.mkv"
                    episodeStr = "OP2"
                break
            else:
                # Generate new random timestamp
                print("Random timestamp", time, "falls within op/ed, retrying.")
        # Check if random timestamp is during outro
        elif time > edStart and time < edEnd:
            if episode == 1 or episode == 12:
                # Calculate equivalent timestamp for creditless video file
                print("Calculating new timestamp for creditless ed.")
                time = round(time - edStart, 2)
                if episode == 1:
                    path = os.getenv('HYOUKA_PATH') + "/Hyouka - NCED1.mkv"
                    episodeStr = "ED1"
                else:
                    path = os.getenv('HYOUKA_PATH') + "/Hyouka - NCED2.mkv"
                    episodeStr = "ED2"
                break
            else:
                # Generate new random timestamp
                print("Random timestamp", time, "falls within op/ed, retrying.")
        else:
            break

    # Grab and save frame
    ffmpeg.input(path, ss=time).filter('scale', width, -1).output("./hyouka_frames/png/Hyouka" + "_ep" + episodeStr + "_" + str(time) + ".png", vframes=1, loglevel="quiet").run()
    ffmpeg.input(path, ss=time).filter('scale', width, -1).output("./hyouka_frames/jpg/Hyouka" + "_ep" + episodeStr + "_" + str(time) + ".jpg", vframes=1, loglevel="quiet").run()

    # Return caption
    caption = episodeStr + " - " + str(round(time)) + "s"

    print(caption)
    return caption


# Function call
# hyoukaGetScreencap()