
import os, argparse
import path, vm

nFRAMES = 2500
datasets = {  # going for 2500 images/movie
    # dataset_name: videoA, intime, duration, fps, videoB, intime, duration, fps
    'm_once2tron':['once-upon-a-time.mp4', '00:20:00', '01:50:00', 'tron.mp4', '00:24:00', '01:30:00'],
    'm_venice2tokyo':['venice.mp4', '00:00:30', '00:44:00', 'tokyo.mp4', '00:00:00', '00:42:00'],
    'm_venice2tron':['venice.mp4', '00:00:30', '00:44:00', 'tron.mp4', '00:24:00', '01:30:00'],
    'm_apollo2tron':['apollo.mp4', '00:00:00', '00:41:00', 'tron.mp4', '00:24:00', '01:30:00'],
    'm_clouds2seastorm':['clouds.mp4', '00:01:40', '03:50:00', 'seastorm.mp4', '00:00:00', '02:30:00'],
    'm_venice2seastorm':['venice.mp4', '00:00:30', '00:44:00', 'seastorm.mp4', '00:00:00', '02:30:00'],
    'm_apollo2odyssey':['apollo.mp4', '00:00:00', '00:41:00', 'a-space-odyssey-hd.mp4', '00:20:00', '01:40:00'],
    'm_animals2clouds':['animals.mp4', '00:30:00', '00:59:00', 'clouds.mp4', '00:01:40', '03:50:00']
    }

def command(txt):
    print "******************************************************************"
    print txt
    os.system(txt)


def calc_fps(dur_str, nFrames):
    h,m,s = dur_str.split(':')
    dur_in_secs = int(h)*3600+int(m)*60+int(s)
    return nFrames/float(dur_in_secs)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    parser.add_argument("--size", dest="size", type=int, default=256)
    parser.add_argument("--fps", dest="fps", type=float, default=24)
    parser.add_argument('--epoch', dest='epoch', type=int, default=200, help='# of epoch')
    parser.add_argument('--num', dest='num', type=int, default=10, help='# of images to generate')
    args = parser.parse_args()

    # if args.cmd == 'prep':
    #     for i,ds in enumerate(datasets.keys()):
    #         path.init(ds)
    #
    #         # del dataset
    #         command('ssh %s "rm /home/stefan/git/%s/%s/*"'\
    #                 % (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.dataset))
    #
    #         # extract
    #         videoA = datasets[ds][0]
    #         videoB = datasets[ds][3]
    #         videoA_in = datasets[ds][1]
    #         videoB_in = datasets[ds][4]
    #         videoA_dur = datasets[ds][2]
    #         videoB_dur = datasets[ds][5]
    #         videoA_fps = calc_fps(videoA_dur, nFRAMES)
    #         videoB_fps = calc_fps(videoB_dur, nFRAMES)
    #         cmd = """cd git/%s; python run.py extract --dataset=%s --size=%s \
    #               --videoA=%s --videoB=%s --videoA_in=%s --videoB_in=%s \
    #               --videoA_dur=%s --videoB_dur=%s --videoA_fps=%s --videoB_fps=%s""" \
    #               % (path.GIT_REPO_NAME, ds, args.size,
    #                  videoA, videoB,
    #                  videoA_in, videoB_in,
    #                  videoA_dur, videoB_dur,
    #                  videoA_fps, videoB_fps)
    #         vm.call_remote_cmd_in_tmux(vm.GPU_INSTANCE, cmd, session_name=ds, debug=False)

    if args.cmd == 'prep_test':
        for i,ds in enumerate(datasets.keys()):
            path.init(ds)

            # extract
            videoA = datasets[ds][0]
            videoB = datasets[ds][3]
            videoA_in = datasets[ds][1]
            videoB_in = datasets[ds][4]
            videoA_dur = datasets[ds][2]
            videoB_dur = datasets[ds][5]
            videoA_fps = calc_fps(videoA_dur, nFRAMES)/10.0
            videoB_fps = calc_fps(videoB_dur, nFRAMES)/10.0
            cmd = """cd git/%s; python run.py extract_test --dataset=%s --size=%s \
                  --videoA=%s --videoB=%s --videoA_in=%s --videoB_in=%s \
                  --videoA_dur=%s --videoB_dur=%s --videoA_fps=%s --videoB_fps=%s""" \
                  % (path.GIT_REPO_NAME, ds, args.size,
                     videoA, videoB,
                     videoA_in, videoB_in,
                     videoA_dur, videoB_dur,
                     videoA_fps, videoB_fps)
            vm.call_remote_cmd_in_tmux(vm.GPU_INSTANCE, cmd, session_name=ds, debug=False)


    elif args.cmd == 'prepcheck':
        for i,ds in enumerate(datasets.keys()):
            path.init(ds)
            print("******* %s" % ds)
            vm.call_remote(vm.GPU_INSTANCE, "ls -1 git/%s/%s | wc -l; ls -1 git/%s/%s | wc -l" % (path.GIT_REPO_NAME, path.trainA, path.GIT_REPO_NAME, path.trainB))


    elif args.cmd == 'train':
        for i,ds in enumerate(datasets.keys()):
            path.init(ds)

            # del checkpoints
            command('ssh %s "rm /home/stefan/git/%s/%s/*"'\
                    % (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.model))

            cmd = "cd git/%s; CUDA_VISIBLE_DEVICES=%s python run.py train --dataset=%s --size=%s --epoch=%s" % (path.GIT_REPO_NAME, i, ds, args.size, args.epoch)
            vm.call_remote_cmd_in_tmux(vm.GPU_INSTANCE, cmd, session_name=ds)


    elif args.cmd == 'runmodels':
        for i,ds in enumerate(datasets.keys()):
            path.init(ds)

            # del test images
            command('ssh %s "rm /home/stefan/git/%s/%s/*"'\
                    % (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.testA))
            command('ssh %s "rm /home/stefan/git/%s/%s/*"'\
                    % (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.testB))

            # copy test images, random, count is args.num
            command('ssh %s "shuf -zn%s -e /home/stefan/git/%s/%s/* | xargs -0 cp -vt /home/stefan/git/%s/%s/"'\
                    % (vm.GPU_INSTANCE, args.num, path.GIT_REPO_NAME, path.trainA, path.GIT_REPO_NAME, path.testA))
            command('ssh %s "shuf -zn%s -e /home/stefan/git/%s/%s/* | xargs -0 cp -vt /home/stefan/git/%s/%s/"'\
                    % (vm.GPU_INSTANCE, args.num, path.GIT_REPO_NAME, path.trainB, path.GIT_REPO_NAME, path.testB))

            cmd = "cd git/%s; CUDA_VISIBLE_DEVICES=%s python run.py test --dataset=%s --size=%s" % (path.GIT_REPO_NAME, i, ds, args.size)
            vm.call_remote_cmd_in_tmux(vm.GPU_INSTANCE, cmd, session_name=ds)


    elif args.cmd == 'pullimages':
        for i,ds in enumerate(datasets.keys()):
            path.init(ds)

            command("rm -r %s" % (path.outA))
            command("rm -r %s" % (path.outB))
            command("mkdir -p %s" % (path.outA))
            command("mkdir -p %s" % (path.outB))
            command("""rsync -rcPz -e ssh %s:/home/stefan/git/%s/%s/ %s""" % \
                    (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.outA, path.outA))
            command("""rsync -rcPz -e ssh %s:/home/stefan/git/%s/%s/ %s""" % \
                    (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.outB, path.outB))


    elif args.cmd == 'pullmodels':
        for i,ds in enumerate(datasets.keys()):
            path.init(ds)

            command("rm -r %s" % (path.model))
            command("mkdir -p %s" % (path.model))
            command("""rsync -rcPz -e ssh %s:/home/stefan/git/%s/%s/ %s""" % \
                    (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.model, path.model))
