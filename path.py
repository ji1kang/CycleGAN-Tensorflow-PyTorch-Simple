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

project = testA = testB = trainA = trainB = model = output = ""
outA = outB = outAjoint = outBjoint = rawA = rawB =""

def init(project_name):
    global project, testA, testB, trainA, trainB, model, output
    global outA, outB, outAjoint, outBjoint, rawA, rawB
    project = os.path.join('datasets', project_name)
    rawA = os.path.join(project, 'rawA')
    rawB = os.path.join(project, 'rawB')
    testA = os.path.join(project, 'testA')
    testB = os.path.join(project, 'testB')
    trainA = os.path.join(project, 'trainA')
    trainB = os.path.join(project, 'trainB')
    model = 'checkpoints'
    output = 'test_predictions'
    outA = os.path.join(output, project_name, 'testA')
    outB = os.path.join(output, project_name, 'testB')
    outAjoint = os.path.join(output, project_name, 'testAjoint')
    outBjoint = os.path.join(output, project_name, 'testBjoint')

    # create
    if not os.path.exists(project):
        os.mkdir(project)
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

    if not os.path.exists(output):
        os.mkdir(output)
    if not os.path.exists(outA):
        os.mkdir(outA)
    if not os.path.exists(outB):
        os.mkdir(outB)
    if not os.path.exists(outAjoint):
        os.mkdir(outAjoint)
    if not os.path.exists(outBjoint):
        os.mkdir(outBjoint)
