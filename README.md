[![License CC BY-NC-SA 4.0](https://img.shields.io/badge/license-CC4.0-blue.svg)](https://raw.githubusercontent.com/NVIDIA/FastPhotoStyle/master/LICENSE.md)
![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)

## FastPhotoStyle

### License
Copyright (C) 2018 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

### About

This code repository contains an implementation of our fast photorealistic style transfer algorithm. Given a content photo and a style photo, the code can transfer the style of the style photo to the content photo. The details of the algorithm behind the code is documented in our arxiv paper. Please cite the paper if this code repository is used in your publications.

[Yijun Li (UC Merced)](https://sites.google.com/site/yijunlimaverick/), [Ming-Yu Liu (NVIDIA)](http://mingyuliu.net/), [Xueting Li (UC Merced)](https://sunshineatnoon.github.io/), [Ming-Hsuan Yang (NVIDIA, UC Merced)](http://faculty.ucmerced.edu/mhyang/), [Jan Kautz (NVIDIA)](http://jankautz.com/) "[A Closed-form Solution to Photorealistic Image Stylization](https://arxiv.org/abs/1802.06474)" arXiv preprint arXiv:1802.06474

![](teaser.png)



### Code usage (Ubuntu with nvidia-docker)

First, install docker (It will also install nvidia-docker2, which we need):
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

Then clone iver56's fork of FastPhotoStyle, which includes a simple REST API web service:

* `git clone https://github.com/iver56/FastPhotoStyle.git`
* `cd FastPhotoStyle`
* `git submodule update --init --recursive`
* `bash download_models.sh`

Build docker image (this typically takes at least 7 minutes, so you might want to grab a coffee or something while you wait):  
`sudo docker build -t fast-photo-style:v1.0 .`

Start the web service inside docker:  
``sudo docker run -d -v `pwd`:/root/FastPhotoStyle --net=host --runtime=nvidia fast-photo-style:v1.0 /opt/anaconda2/bin/python /root/FastPhotoStyle/web_service.py``

You can now access the REST API on port 5000
