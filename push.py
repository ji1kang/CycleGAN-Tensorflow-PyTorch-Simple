
import os, argparse
import path, vm


# datasets = ['cats2clouds', 'porn2figure', 'porn2flora', 'porn2miami', 'porn2schiele', 'selfies2astro', 'selfies2illust', 'selfies2renaiss']
datasets = ['cats2clouds']


def command(txt):
    print "******************************************************************"
    print txt
    os.system(txt)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", action='store_true')
    args = parser.parse_args()

    INSTANCE = vm.RELAY_INSTANCE
    if args.gpu:
        INSTANCE = vm.GPU_INSTANCE


    for ds in datasets:
        path.init(ds)

        # mkdir datasets
        command('ssh %s "mkdir -p /home/stefan/git/%s/%s; mkdir -p /home/stefan/git/%s/%s;"'\
                % (INSTANCE, path.GIT_REPO_NAME, path.trainA, path.GIT_REPO_NAME, path.trainB))

        # trainA
        command("""rsync -rcPz -e ssh --delete %s/ %s:/home/stefan/git/%s/%s/""" \
                % (path.trainA, INSTANCE, path.GIT_REPO_NAME, path.trainA))

        # trainB
        command("""rsync -rcPz -e ssh --delete %s/ %s:/home/stefan/git/%s/%s/""" \
                % (path.trainB, INSTANCE, path.GIT_REPO_NAME, path.trainB))
