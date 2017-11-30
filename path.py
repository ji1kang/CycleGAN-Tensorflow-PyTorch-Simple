"""Manage the directories of a roject.

Directories are as follows:
    datasets/                 ... home of all the data
    datasets/<name>           ... a specific dataset
    ---
    datasets/<name>/testA     ... test A images
    datasets/<name>/testA     ... test B images
    datasets/<name>/testA     ... train A images
    datasets/<name>/testA     ... train B images
    checkpoint/               ... model
    test/                     ... model output
"""

import os
import shutil

GIT_REPO_URL = "https://github.com/nortd/CycleGAN_Tensorlayer.git"
GIT_REPO_NAME = "CycleGAN_Tensorlayer"

project = testA = testB = trainA = trainB = model = output = ""

def init(project_name):
    global project, testA, testB, trainA, trainB, model, output
    project = os.path.join('datasets', project_name)
    testA = os.path.join(project, 'testA')
    testB = os.path.join(project, 'testB')
    trainA = os.path.join(project, 'trainA')
    trainB = os.path.join(project, 'trainB')
    model = 'checkpoint'
    test = 'test'
    output = 'output'

    # create
    if not os.path.exists(project):
        os.mkdir(project)
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
    if not os.path.exists(test):
        os.mkdir(test)
    if not os.path.exists(output):
        os.mkdir(output)
