
import os, argparse
import path, vm

SIZE = 256
EPOCHS = 200
# datasets = ['cats2clouds', 'porn2figure', 'porn2flora', 'porn2miami', 'porn2schiele', 'selfies2astro', 'selfies2illust', 'selfies2renaiss']
datasets = ['m_once2tron', 'm_venice2tokyo', 'm_venice2tron', 'm_apollo2tron', 'm_clouds2seastorm', 'm_venice2seastorm', 'm_apollo2odyssey', 'm_animals2clouds']

def command(txt):
    print "******************************************************************"
    print txt
    os.system(txt)


if __name__ == "__main__":
    for i,ds in enumerate(datasets):
        path.init(ds)

        # del checkpoints
        command('ssh %s "rm /home/stefan/git/%s/%s/*"'\
                % (vm.GPU_INSTANCE, path.GIT_REPO_NAME, path.model))

        cmd = "cd git/%s; CUDA_VISIBLE_DEVICES=%s python run.py train --dataset=%s --size=%s --epoch=%s" % (path.GIT_REPO_NAME, i, ds, SIZE, EPOCHS)
        vm.call_remote_cmd_in_tmux(vm.GPU_INSTANCE, cmd, session_name=ds)
