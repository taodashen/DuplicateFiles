#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2017, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : duplicateFiles.py 
@Time    : 2019/2/17 12:37 
@Desc    : 
"""

import os
import sys
import hashlib


# 获取所有文件的文件名
def get_files_list(path):
    filename_list = os.listdir(path=path)
    return filename_list
    pass


# 获取文件的MD5值
def get_md5(filepath, filename):
    filepath = os.path.join(filepath, filename)
    file_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            origin = f.read(2048)
            if not origin:
                break
            file_md5.update(origin)
    return file_md5.hexdigest()
    pass


# 获取所有文件的MD5值
def get_files_md5(path):
    file_list = get_files_list(path)
    result = []
    md5_list = []
    for filename in file_list:
        # 该路径是文件
        abs_filepath = os.path.join(path, filename)
        if os.path.isfile(abs_filepath):
            md5 = get_md5(path, filename)
            if md5 not in md5_list:
                md5_list.append(md5)
                result.append([abs_filepath])
                continue
            else:
                index = md5_list.index(md5)
                result[index].append(abs_filepath)
        # 该路径是文件夹
        else:
            handle_exist_dir(path + '\\' + filename, md5_list=md5_list, result=result)
            pass
    return md5_list, result
    pass


# 获取所有文件的MD5值, 用于存在文件夹的递归处理
def handle_exist_dir(path, md5_list, result):
    file_list = get_files_list(path)
    for filename in file_list:
        # 该路径是文件
        abs_filepath = os.path.join(path, filename)
        if os.path.isfile(abs_filepath):
            md5 = get_md5(path, filename)
            if md5 not in md5_list:
                md5_list.append(md5)
                result.append([abs_filepath])
                continue
            else:
                index = md5_list.index(md5)
                result[index].append(abs_filepath)
        # 该路径是文件夹
        else:
            handle_exist_dir(path + '\\' + filename, md5_list=md5_list, result=result)
            pass
    return md5_list, result
    pass


# 获取重复文件, 删除重复的文件
def del_duplicate_files(path):
    md5, name_list = get_files_md5(path)
    for item in name_list:
        for i in range(1, len(item)):
            # file_path = path + item[i]
            if os.path.exists(item[i]):
                print("正在删除 {}".format(item[i]))
                os.remove(item[i])
                pass
    return md5, name_list
    pass


# 删除重复文件
def main(argv):
    if len(argv) > 1:
        path = argv[1] + '\\'
    else:
        path = os.getcwd() + '\\test'
    print("正在扫描目录 {} 下的所有文件，请稍等…".format(path))
    none, result = get_files_md5(path)
    for item in result:
        for i in range(1, len(item)):
            absfilepath = os.path.join(path, item[i])
            print("扫描到重复文件： {}".format(absfilepath))
    option = input("请确认删除[Y]/N: ")
    if option == 'Y' or option == 'y':
        del_duplicate_files(path)
        print("删除成功。")
    else:
        print("退出成功。")
    pass


if __name__ == "__main__":
    print("*******************  Welcome to duplicate files tools  *********************")
    main(sys.argv)
    pass
