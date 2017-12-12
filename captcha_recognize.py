from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import os.path
from datetime import datetime
from PIL import Image
import numpy as np

import tensorflow as tf
from tensorflow.python.platform import gfile
import captcha_model as captcha

import config

import cStringIO,  requests, random , string

IMAGE_WIDTH = config.IMAGE_WIDTH
IMAGE_HEIGHT = config.IMAGE_HEIGHT

CHAR_SETS = config.CHAR_SETS
CLASSES_NUM = config.CLASSES_NUM
CHARS_NUM = config.CHARS_NUM

checkpoint_dir = "./captcha_train"

def one_hot_to_texts(recog_result):
  texts = []
  for i in xrange(recog_result.shape[0]):
    index = recog_result[i]
    texts.append(''.join([CHAR_SETS[i] for i in index]))
  return texts


def getImage(url_yzm):
  s = requests.session()
  img = Image.open(cStringIO.StringIO(s.get(url_yzm).content))
  return img


def input_data(image_dir):
  if not gfile.Exists(image_dir):
    print(">> Image director '" + image_dir + "' not found.")
    return None
  extensions = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG']
  print(">> Looking for images in '" + image_dir + "'")
  file_list = []
  for extension in extensions:
    file_glob = os.path.join(image_dir, '*.' + extension)
    file_list.extend(gfile.Glob(file_glob))
  if not file_list:
    print(">> No files found in '" + image_dir + "'")
    return None
  batch_size = len(file_list)
  images = np.zeros([batch_size, IMAGE_HEIGHT*IMAGE_WIDTH], dtype='float32')
  files = []
  i = 0
  for file_name in file_list:
    image = Image.open(file_name)
    image_gray = image.convert('L')
    image_resize = image_gray.resize(size=(IMAGE_WIDTH,IMAGE_HEIGHT))
    image.close()
    input_img = np.array(image_resize, dtype='float32')
    input_img = np.multiply(input_img.flatten(), 1./255) - 0.5    
    images[i,:] = input_img
    base_name = os.path.basename(file_name)
    files.append(base_name)
    i += 1
  return images, files


def run_predict(url_yzm):
  with tf.Graph().as_default(), tf.device('/cpu:0'):
    input_images = [getImage(url_yzm)]
    images = tf.constant(input_images)
    logits = captcha.inference(images, keep_prob=1)
    result = captcha.output(logits)
    saver = tf.train.Saver()
    sess = tf.Session()
    saver.restore(sess, tf.train.latest_checkpoint(checkpoint_dir))
    print(tf.train.latest_checkpoint(checkpoint_dir))
    recog_result = sess.run(result)
    sess.close()
    text = one_hot_to_texts(recog_result)
    total_count = len(input_images)
    true_count = 0.
    for i in range(total_count):
      print('image ' + input_images[i] + " recognize ----> '" + text[i] + "'")

if __name__ == '__main__':
  url_yzm="https://jy.xzsec.com/Login/YZM?randNum=0.5609794557094574"
  run_predict(url_yzm)