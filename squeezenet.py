#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:37:36 2018

@author: phoenix
"""

# import everything
from __future__ import print_function, division
import torchvision
from torchvision.datasets import ImageFolder
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import copy
import os

# dataset format
"""
structure of dataset folder
	root/dog/xxx.png
    root/dog/xxy.png
    root/dog/xxz.png
    root/cat/123.png
    root/cat/nsdf3.png
    root/cat/asd932_.png
"""

"""
we're using these transforms before passing the images
in the dataset for training and validation
"""
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
transforms = transforms.Compose([
                            transforms.RandomHorizontalFlip(),
                            transforms.ToTensor(),
                            normalize,
                        ])

# path of dataset: train and test directory
root = '<your folder>'
traindir = root+'/train/'
testdir = root+'/test/'
# number of classes in the dataset
num_of_output_classes = 104

# HYPER-PARAMETERS
num_epochs = 10
train_only_last_layer = False # boolean variable
""" you can use both 'squeeznet' 
 'squeezenet1_0',
 'squeezenet1_1']
NOTE: Squeeznet does not have linear layer in the last. 
we modify the Conv2d layer present in the end to give output
according the number of classes we have
 """
# example
model_conv = torchvision.models.squeezenet1_1(pretrained=True) # define model here

# Load dataset
train_data = datasets.ImageFolder(traindir, transforms)
test_data =  datasets.ImageFolder(testdir, transforms)

# some variables storing dataset info
dset_sizes = {} # empty dict
dset_sizes['train'] = len(train_data)
dset_sizes['val'] = len(test_data)
dset_classes = train_data.classes # number of classes in datasets

# create training and validation loaders for passing to model
train_loader = torch.utils.data.DataLoader(
                        train_data,
                        batch_size=15,
                        shuffle=True,
                        num_workers=4,
                        pin_memory=True)

val_loader = torch.utils.data.DataLoader(
                        test_data,
                        batch_size=5,
                        shuffle=False,
                        num_workers=4,
                        pin_memory=True)


# Train on GPU if CUDA is available
use_gpu = torch.cuda.is_available()


"""Use this if you want to visualise the dataset before training"""

# Get a batch of training data
inputs, classes = next(iter(train_loader))

# Make a grid from batch
out = torchvision.utils.make_grid(inputs)

# imshow(out, title=[dset_classes[x] for x in classes])

#+++++++++++++++++++++++++++++++++++++++
# USELESS FUNCTIONS HERE
#+++++++++++++++++++++++++++++++++++++++

# UTILITY FUNCTIONS HERE.

######################################################################
# Learning rate scheduler
# ^^^^^^^^^^^^^^^^^^^^^^^
# Let's create our learning rate scheduler. We will exponentially
# decrease the learning rate once every few epochs.

"""This function is useful only if using SGD otherwise no use"""

def exp_lr_scheduler(optimizer, epoch, init_lr=0.001, lr_decay_epoch=7):
    """Decay learning rate by a factor of 0.1 every lr_decay_epoch epochs."""
    lr = init_lr * (0.1**(epoch // lr_decay_epoch))

    if epoch % lr_decay_epoch == 0:
        print('LR is set to {}'.format(lr))

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

    return optimizer

# utility function to visualise few images from the dataset
def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    plt.imshow(inp)
    # if title is not None:
        # plt.title(title)
    plt.pause(10)  # pause a bit so that plots are updated


######################################################################
# Visualizing the model predictions
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Generic function to display predictions for a few images
#

def visualize_model(model, num_images=6):
    images_so_far = 0
    fig = plt.figure()

    for i, data in enumerate(val_loader):
        inputs, labels = data
        if use_gpu:
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
        else:
            inputs, labels = Variable(inputs), Variable(labels)

        outputs = model(inputs)
        _, preds = torch.max(outputs.data, 1)

        for j in range(inputs.size()[0]):
            images_so_far += 1
            ax = plt.subplot(num_images//2, 2, images_so_far)
            ax.axis('off')
            ax.set_title('predicted: {}'.format(dset_classes[labels.data[j]]))
            imshow(inputs.cpu().data[j])

            if images_so_far == num_images:
                return





######################################################################
# Training the model
# ------------------
#
# -  Saving (deep copying) the best model
#
# In the following, parameter ``lr_scheduler(optimizer, epoch)``
# is a function  which modifies ``optimizer`` so that the learning
# rate is changed according to desired schedule.

def train_model(model, criterion, optimizer, lr_scheduler, num_epochs=25):
    since = time.time()

    best_model = model
    best_acc = 0.0

    # run for given number of epochs
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                optimizer = lr_scheduler(optimizer, epoch)
                model.train(True)  # Set model to training mode
            else:
                model.train(False)  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            if phase == 'train':
                phase_ = train_loader
            else:
                phase_ = val_loader

            # Run through all data in mini batches
            for data in phase_:
                # get the inputs
                inputs, labels = data

                # wrap them in Variable
                if use_gpu:
                    inputs, labels = Variable(inputs.cuda()), \
                        Variable(labels.cuda())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward pass
                outputs = model(inputs)
                _, preds = torch.max(outputs.data, 1)

                # calculating the loss
                loss = criterion(outputs, labels)

                # backward + optimize only if in training phase
                if phase == 'train':
                    loss.backward()
                    optimizer.step()

                # statistics for printing
                running_loss += loss.data[0]
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dset_sizes[phase]
            epoch_acc = running_corrects / dset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # save model if it performed better than
            # any other previous model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model = copy.deepcopy(model)

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))
    return best_model


######################################################################
# ConvNet training
# ----------------------------------
"""
We use a pre-trained model here and replace it's last fully connected
according to the number of classes in our dataset.
Also, we only train the last layer of the model and keep all the other
weights as it is.
"""

# using the model defined in the beginning of the program
# Example: model_conv = torchvision.models.resnet18(pretrained=True)


if train_only_last_layer is True:
	# turn off backprop update for all the weights in the model
	for param in model_conv.parameters():
	    param.requires_grad = False

# change the last Conv2D layer in case of squeezenet. there is no fc layer in the end.
num_ftrs = 512
model_conv.classifier._modules["1"] = nn.Conv2d(512, num_of_output_classes, kernel_size=(1, 1))

# because in forward pass, there is a view function call which depends on the final output class size.
model_conv.num_classes = num_of_output_classes


if use_gpu:
    model_conv = model_conv.cuda()

# defining loss criterion, for these
# models CrossEntropyLoss works the best
criterion = nn.CrossEntropyLoss()

# Observe that only parameters of final layer are being optimized as
# opoosed to before.
""" Defining an optimiser function here, can use Adam, RMSprop or simple SGD"""
optimizer_conv = optim.SGD(model_conv.classifier.parameters(), lr=0.001, momentum=0.9)


######################################################################
# Train and evaluate
# ^^^^^^^^^^^^^^^^^^
model_conv = train_model(model_conv, criterion, optimizer_conv,
                         exp_lr_scheduler, num_epochs=num_epochs)

######################################################################

# If we want to visvalise model. then call this function
# visualize_model(model_conv)

# plt.ioff()
# plt.show()