"""Run NN through various phases.

1. 'extract' images from video.
2. 'prep' training set
3. 'train' model
4. 'test' model
5. 'videofy' output
"""

import os
import glob
import shutil
import argparse

import path
import vm
import imageslicer

# PROJECT = "enhance2"
PROJECT = "odyssey2ghost"
VIDEO_A = "../../../../a-space-odyssey.mp4"
VIDEO_B = "../../../../ghost-in-the-shell.mp4"
# TRAINGVIDEO_FPS = "1/4"
TRAINGVIDEO_FPS = "1/10"

path.init(PROJECT)



def push(project_name):
    """Push training set to GPU_INSTANCE."""
    cmd = """rsync -rcP -e ssh --delete %s %s:/home/stefan/git/%s/datasets/%s/""" % \
          (path.project, vm.GPU_INSTANCE, path.GIT_REPO_NAME, project_name)
    os.system(cmd)


def pull(project_name):
    """Pull trained model from GPU_INSTANCE."""
    cmd = """rsync -rcP -e ssh --delete %s:/home/stefan/git/%s/%s/ %s""" % \
          (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.model, path.model)
    os.system(cmd)



def video_extract(video_path, out_path, fps, scale="-2:256", intime="", duration="", pattern="image%05d.jpg"):
    cwd = os.getcwd()
    os.chdir(out_path)
    fps = "-r %s" % (fps)
    filepattern = pattern
    if scale != "":
        scale = '-vf "crop=in_h:in_h,scale=%s"' % (scale)
    if intime != "":
        intime = "-ss %s" % (intime)
    if duration != "":
        duration = "-t %s" % (duration)
    cmd = 'ffmpeg %s %s -i %s %s %s -f image2  -q:v 2 %s' % (intime, duration, video_path, scale, fps, filepattern)
    # cmd = """ffmpeg -i ../video.mp4  -r 1/2  -f image2  -q:v 2 image%05d.jpg"""
    print cmd
    os.system(cmd)
    os.chdir(cwd)

def video_make(img_path, video_path, fps=30, quality=15, pattern="image%d.jpg"):
    cwd = os.getcwd()
    os.chdir(img_path)
    # cmd = "ffmpeg -r 30 -f image2 -s 256x256 -i pic_%d-outputs.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ../out.mp4"
    cmd = 'ffmpeg -r %s -i %s -c:v libx264 -crf %s -vf "fps=%s,format=yuv420p" %s'\
          % (fps, pattern, quality, fps, video_path)
    os.system(cmd)
    os.chdir(cwd)




parser = argparse.ArgumentParser()
# parser.add_argument("project", choices=projects)
parser.add_argument("cmd", choices=['extract', 'train', 'testprep', 'test', 'push', 'pull', 'tilejoin', 'videofy'])
# parser.add_argument("--epochs", dest="epochs", type=int, default=200)
# parser.add_argument("--size", dest="size", type=int, default=256)
args = parser.parse_args()


if args.cmd == 'extract':
    # video_extract(VIDEO_A, path.trainA, TRAINGVIDEO_FPS, intime="00:20:00", duration="01:00:00", scale="-2:512")
    video_extract(VIDEO_A, path.trainA, TRAINGVIDEO_FPS, intime="00:20:00", duration="01:00:00")
    video_extract(VIDEO_B, path.trainB, TRAINGVIDEO_FPS, intime="00:15:00", duration="01:00:00")
    for img in glob.glob(os.path.join(path.trainA,"*.jpg")):
        shutil.copy(img, path.testA)
    for img in glob.glob(os.path.join(path.trainB,"*.jpg")):
        shutil.copy(img, path.testB)
elif args.cmd == 'train':
    os.system("python train.py --dataset=odyssey2ghost --load_size=256 --crop_size=256")
elif args.cmd == 'testprep':
    for img in glob.glob(os.path.join(path.trainA,"*.jpg")):
        imageslicer.slice(img, 4, path.testA)
    # shutil.copy(path.trainB, path.testB)
elif args.cmd == 'test':
    os.system("python test.py")
elif args.cmd == 'push':
    push(PROJECT)
elif args.cmd == 'pull':
    pull(PROJECT)
elif args.cmd == 'tilejoin':
    imageslicer.joinall(path.testA, path.output)
elif args.cmd == 'videofy':
    video_make(path.output, "out.mp4", pattern="image%d.jpg")
