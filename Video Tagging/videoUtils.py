import os
import subprocess
import shutil


def videoFrames(filename, framerate=1):
    """
    Returns a generator of frames from a video specified by FILEPATH
    """
    vid_file = os.path.join(os.path.dirname(os.getcwd()), "Database", "Video", filename)
    print(vid_file)
    assert os.path.isfile(vid_file), "Given path is not a valid file"
    tmpdir = os.path.join(os.getcwd(), "tmp")
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.mkdir(tmpdir)
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            vid_file,
            "-r",
            f"{framerate}",
            os.path.join(tmpdir, "img_%04d.jpg"),
        ]
    )
    return [os.path.join(tmpdir, i) for i in os.listdir(tmpdir)]

