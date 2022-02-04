import glob
import os
import subprocess

import requests

import oa.util.legacy

from oa.util.abilities.core import info

def download_file(url, path):
    """ Download a file by url and save it to a local path. """
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def find_file(fname):
    """ Search for a file with `fname` in all OA sub-directories.
        Able to use a short name if it is unique.
        NEED FIX - Put file names into Cache list ? """
    core_directory = oa.util.legacy.core_directory
    ret = glob.glob(os.path.join(core_directory,'modules/mind/minds/*/%s' %fname))
    if not ret:
        ret = glob.glob(os.path.join(core_directory,'modules/mind/minds/*/*/%s' %fname))
    if len(ret) != 1:
        raise Exception('%s: found %d results.' %(fname, len(ret)))
    return ret[0]

def read_file(fname, result_as_list = 0):
    """ Read the contents of a file and return a string or a list of strings split by a new line symbol. """
    try:
        info('- Reading file: ', fname)
        if not os.path.exists(fname):
            fname = find_file(fname)
        with open(fname, 'r') as f:
            if result_as_list:
                return f.readlines()
            else:
                return f.read()
    except: # FileNotFoundError:
        info("- Error loading file: {path}".format(path = fname))
        # logger.warn("Error loading file: {path}".format(path = fname))
        return ''

def write_file(fname, data, append = False):
    """ Write data to a file. """
    if append:
        with open(fname, 'w+') as f:
            f.write(data)
    else:
        with open(fname, 'w') as f:
            f.write(data)


def stat_size(fname):
    """ Return a file size. """
    return os.stat(fname).st_size

def stat_mtime(fname):
    """ Return the last modification time of a file in seconds. """
    return os.stat(fname).st_mtime

def sys_exec(cmd):
    """ Execute a command. """
    subprocess.call(cmd, shell = True)