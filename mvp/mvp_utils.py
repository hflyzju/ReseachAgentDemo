import os
def safe_mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)