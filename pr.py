#! /bin/python

import os
import args
import exif
import shutil
from os import path


def file_or_dir(p):
    if path.isdir(p):
        return 'dir'
    elif path.isfile(p):
        return 'file'
    else:
        raise

args = args.args_proc()
src_path = os.path.abspath(args['src'])
dst_path = os.path.abspath(args['dst'])
src_path_type = file_or_dir(src_path)
dst_path_type = file_or_dir(dst_path)
if src_path == dst_path:
    rename = os.rename
else:
    rename = shutil.copy2
src_file_list = os.listdir(src_path)
pre_name = ''
for src_file in src_file_list:
    src_file = os.path.join(src_path, src_file)
    if path.isfile(src_file):
        f = exif.exif(src_file)
        filetype = f.detect_filetype()
        if filetype != 'unknown':
            name = f.read_tag_datetimeoriginal()
            dst_file = os.path.join(dst_path, name)
            #f.close()
            if pre_name != name:
                dup_count = 0
            else:
                dup_count += 1
                dst_file = dst_file.join(['-', dup_count])
            dst_file += '.'
            dst_file += filetype
            rename(src_file, dst_file)
