"""Manage the directories of a roject.

Directories are as follows:
    datasets/                 ... home of all the data
    datasets/<name>           ... a specific dataset
    ---
    datasets/<name>/testA     ... test A images
    datasets/<name>/testA     ... test B images
    datasets/<name>/testA     ... train A images
    datasets/<name>/testA     ... train B images
    checkpoints/               ... model
    test/                     ... model output
"""

import os
import shutil

GIT_REPO_URL = "https://github.com/nortd/CycleGAN-Tensorflow-PyTorch-Simple.git"
GIT_REPO_NAME = "CycleGAN-Tensorflow-PyTorch-Simple"

dataset = testA = testB = trainA = trainB = model = ""
outA = outB = outAjoint = outBjoint = rawA = rawB =""

def init(project_name):
    global dataset, testA, testB, trainA, trainB, model, output
    global outA, outB, outAjoint, outBjoint, rawA, rawB
    dataset = os.path.join('datasets', project_name)
    rawA = os.path.join(dataset, 'rawA')
    rawB = os.path.join(dataset, 'rawB')
    testA = os.path.join(dataset, 'testA')
    testB = os.path.join(dataset, 'testB')
    trainA = os.path.join(dataset, 'trainA')
    trainB = os.path.join(dataset, 'trainB')
    model = os.path.join('checkpoints',project_name)
    outA = os.path.join(dataset, 'outA')
    outB = os.path.join(dataset, 'outB')
    outAjoint = os.path.join(dataset, 'outAjoint')
    outBjoint = os.path.join(dataset, 'outBjoint')

    # create
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    if not os.path.exists(rawA):
        os.mkdir(rawA)
    if not os.path.exists(rawB):
        os.mkdir(rawB)
    if not os.path.exists(testA):
        os.mkdir(testA)
    if not os.path.exists(testB):
        os.mkdir(testB)
    if not os.path.exists(trainA):
        os.mkdir(trainA)
    if not os.path.exists(trainB):
        os.mkdir(trainB)
    if not os.path.exists(model):
        os.mkdir(model)
    if not os.path.exists(outA):
        os.mkdir(outA)
    if not os.path.exists(outB):
        os.mkdir(outB)
    if not os.path.exists(outAjoint):
        os.mkdir(outAjoint)
    if not os.path.exists(outBjoint):
        os.mkdir(outBjoint)
