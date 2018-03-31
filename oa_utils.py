import os, sys
import subprocess, requests

def exec_cmd(cmd):
    """print cmd execute in OS env"""
    print('Execute : '+cmd)
    subprocess.call(cmd, shell=True)

def download_file(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def fwrite(fname, data, append=False):
        #no max_size analyze for now.
        #FIX : in case of max_size -> use LIFO
#        if os.path.exists(fname):
#            if os.stat(fname).st_size
    if append:
        with open(fname, 'w+') as f:
            f.write(data)
    else:
        with open(fname, 'wb') as f:
            f.write(data)

def fread(fname):
    try:
        with open(fname, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        logger.warn("Error loading file: {path}".format(path=fname))
        return ''

def stat_size(fname):
    """
      returns file size
    """
    return os.stat(fname).st_size

def stat_mtime(fname):
    """
      returns file last modification time (in seconds)
    """
    return os.stat(fname).st_mtime

#def make_dirs(_, directory):
#    if not os.path.exists(directory):
#        os.makedirs(directory)
