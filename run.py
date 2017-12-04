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
VIDEO_A = "../../../../a-space-odyssey-hd.mp4"
VIDEO_B = "../../../../ghost-in-the-shell.mp4"
# TRAINGVIDEO_FPS = "1/4"
TRAINGVIDEO_FPS = "1/10"

path.init(PROJECT)


def push(project_name):
    """Push training set to GPU_INSTANCE."""
    cmd = """rsync -rcPz -e ssh --delete %s %s:/home/stefan/git/%s/datasets/%s/""" % \
          (path.project, vm.GPU_INSTANCE, path.GIT_REPO_NAME, project_name)
    os.system(cmd)


def pull(project_name):
    """Pull trained model from GPU_INSTANCE."""
    cmd = """rsync -rcPz -e ssh --delete %s:/home/stefan/git/%s/%s/ %s""" % \
          (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.model, path.model)
    print(cmd)
    os.system(cmd)



def video_extract(video_path, out_path, fps, size=256, intime="", duration="", pattern="img%05d.jpg"):
    cwd = os.getcwd()
    os.chdir(out_path)
    fps = "-r %s" % (fps)
    filepattern = pattern
    if size != "":
        size = '-vf "crop=in_h:in_h,scale=-2:%s"' % (size)
    if intime != "":
        intime = "-ss %s" % (intime)
    if duration != "":
        duration = "-t %s" % (duration)
    cmd = 'ffmpeg %s %s -i %s %s %s -f image2  -q:v 2 %s' % (intime, duration, video_path, size, fps, filepattern)
    # cmd = """ffmpeg -i ../video.mp4  -r 1/2  -f image2  -q:v 2 image%05d.jpg"""
    print cmd
    os.system(cmd)
    os.chdir(cwd)

def video_make(img_path, video_path, fps=30, quality=15, pattern="img%d.jpg"):
    cwd = os.getcwd()
    os.chdir(img_path)
    # cmd = "ffmpeg -r 30 -f image2 -s 256x256 -i pic_%d-outputs.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ../out.mp4"
    cmd = 'ffmpeg -r %s -i %s -c:v libx264 -crf %s -vf "fps=%s,format=yuv420p" %s'\
          % (fps, pattern, quality, fps, video_path)
    os.system(cmd)
    os.chdir(cwd)


def delete_files(path):
    for name in os.listdir(path):
        fullname = os.path.join(path,name)
        if os.path.isfile(fullname):
            os.unlink(fullname)


parser = argparse.ArgumentParser()
# parser.add_argument("project", choices=projects)
parser.add_argument("cmd", choices=['extract', 'train', 'testprep', 'test', 'push', 'pull', 'tilejoin', 'videofy'])
# parser.add_argument("--epochs", dest="epochs", type=int, default=200)
parser.add_argument("--size", dest="size", type=int, default=256)
parser.add_argument("--tiles", dest="tiles", type=int, default=4)
args = parser.parse_args()


if args.cmd == 'extract':
    delete_files(path.rawA)
    video_extract(VIDEO_A, path.rawA, 24, size=args.size, intime="00:50:00", duration="00:04:40")

    # delete_files(path.trainA)
    # delete_files(path.trainB)
    # video_extract(VIDEO_A, path.trainA, TRAINGVIDEO_FPS, size=args.size, intime="00:20:00", duration="01:00:00")
    # video_extract(VIDEO_B, path.trainB, TRAINGVIDEO_FPS, size=args.size, intime="00:15:00", duration="01:00:00")

    # for img in glob.glob(os.path.join(path.trainA,"*.jpg")):
    #     shutil.copy(img, path.rawA)
    # for img in glob.glob(os.path.join(path.trainB,"*.jpg")):
    #     shutil.copy(img, path.rawB)
elif args.cmd == 'train':
    os.system("python train.py --dataset=%s --load_size=%s --crop_size=%s" % (PROJECT, args.size, args.size))
elif args.cmd == 'testprep':
    delete_files(path.testA)
    imageslicer.sliceall(path.rawA, save_path=path.testA, nTiles=args.tiles, fit_size=(args.size, args.size), prefix="img%05d")
    # shutil.copy(path.trainB, path.testB)
elif args.cmd == 'test':
    delete_files(path.outA)
    delete_files(path.outB)
    os.system("python test.py --dataset=%s --crop_size=%s" % (PROJECT, args.size))
elif args.cmd == 'push':
    push(PROJECT)
elif args.cmd == 'pull':
    pull(PROJECT)
elif args.cmd == 'tilejoin':
    delete_files(path.outAjoint)
    imageslicer.joinall(path.outA, path.outAjoint)
elif args.cmd == 'videofy':
    video_make(path.outAjoint, "out.mp4", pattern="img%d.jpg")
