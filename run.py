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


VIDEO_A = "../../../../a-space-odyssey-hd.mp4"
VIDEO_B = "../../../../ghost-in-the-shell.mp4"




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


def enumerate_files(path, pattern="img%05d"):
    for i,name in enumerate(os.listdir(path)):
        fullname = os.path.join(path,name)
        if os.path.isfile(fullname):
            os.rename(fullname, os.path.join(path,(pattern+'.jpg')%(i)))

def delete_files(path):
    for name in os.listdir(path):
        fullname = os.path.join(path,name)
        if os.path.isfile(fullname):
            os.unlink(fullname)


parser = argparse.ArgumentParser()
parser.add_argument("cmd")
# parser.add_argument("--epochs", dest="epochs", type=int, default=200)
parser.add_argument("--dataset", dest="dataset", default="porn2schiele")
parser.add_argument("--size", dest="size", type=int, default=256)
parser.add_argument("--tiles", dest="tiles", type=int, default=1)
parser.add_argument("--fps", dest="fps", type=float, default=24)
args = parser.parse_args()

path.init(args.dataset)


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
elif args.cmd == 'cleanraw':
    enumerate_files(path.rawA)
    enumerate_files(path.rawB)
elif args.cmd == 'trainprep':
    delete_files(path.trainA)
    imageslicer.sliceall(path.rawA, save_path=path.trainA, nTiles=args.tiles, fit_size=(args.size, args.size), prefix="img%05d")
    delete_files(path.trainB)
    imageslicer.sliceall(path.rawB, save_path=path.trainB, nTiles=args.tiles, fit_size=(args.size, args.size), prefix="img%05d")
elif args.cmd == 'train':
    os.system("python train.py --dataset=%s --load_size=%s --crop_size=%s" % (args.dataset, args.size, args.size))
elif args.cmd == 'testprep':
    delete_files(path.testA)
    imageslicer.sliceall(path.rawA, save_path=path.testA, nTiles=args.tiles, fit_size=(args.size, args.size), prefix="img%05d")
    # shutil.copy(path.trainB, path.testB)
elif args.cmd == 'test':
    delete_files(path.outA)
    delete_files(path.outB)
    os.system("python test.py --dataset=%s --crop_size=%s" % (args.dataset, args.size))
elif args.cmd == 'pushdataset':
    """Push training set to GPU_INSTANCE."""
    cmd = """rsync -rcPz -e ssh --delete %s %s:/home/stefan/git/%s/%s/""" % \
          (path.dataset, vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.dataset)
    os.system(cmd)
elif args.cmd == 'pulldataset':
    cmd = """rsync -rcPz -e ssh --delete %s:/home/stefan/git/%s/%s/ %s""" % \
    (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.dataset, path.dataset)
    print(cmd)
    os.system(cmd)
elif args.cmd == 'pullmodel':
    """Pull trained model from GPU_INSTANCE."""
    cmd = """rsync -rcPz -e ssh --delete %s:/home/stefan/git/%s/%s/ %s""" % \
          (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.model, path.model)
    print(cmd)
    os.system(cmd)
elif args.cmd == 'tilejoin':
    delete_files(path.outAjoint)
    imageslicer.joinall(path.outA, path.outAjoint)
elif args.cmd == 'videofy':
    video_make(path.outA, "../out.mp4", fps=args.fps, pattern="img%05d.jpg")
