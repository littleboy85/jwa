import os, sys

DEBUG = True

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)

WATERMARK_PATH = os.path.join(ROOT_PATH, '..', 'lib', 'image', 'watermark.png')
