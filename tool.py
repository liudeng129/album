#coding: utf-8
from PIL import Image
import os
import sys
import json
from datetime import datetime
from ImageProcess import Graphics

# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0


def make_directory(directory):
    """创建目录"""
    os.makedirs(directory)

def directory_exists(directory):
    """判断目录是否存在"""
    if os.path.exists(directory):
        return True
    else:
        return False

def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        name, fileformat = filename.split(".")
        if fileformat.lower() == "jpg" or fileformat.lower() == "png" or fileformat.lower() == "gif":
            new_list.append(filename)
    # print new_list
    return new_list


def print_help():
    print("""
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
    1) normal compress(4M to 1M around)
    2) small compress(4M to 500K around)
    3) smaller compress(4M to 300K around)
    """)

def compress(choose, des_dir, src_dir, file_list):
    """压缩算法，img.thumbnail对图片进行压缩，

    参数
    -----------
    choose: str
            选择压缩的比例，有4个选项，越大压缩后的图片越小
    """
    if choose == '1':
        scale = SIZE_normal
    if choose == '2':
        scale = SIZE_small
    if choose == '3':
        scale = SIZE_more_small
    if choose == '4':
        scale = SIZE_more_small_small
    for infile in file_list:
        img = Image.open(des_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        img.save(des_dir + infile)

def compress_photo():
    '''调用压缩图片的函数
    '''
    src_dir, des_dir = "photos/", "min_photos/"

    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list_src = list_img_file(src_dir)
    if directory_exists(des_dir):
        if not directory_exists(des_dir):
            make_directory(des_dir)
        file_list_des = list_img_file(des_dir)
        # print file_list
    '''如果已经压缩了，就不再压缩'''
    for i in range(len(file_list_des)):
        if file_list_des[i] in file_list_src:
            file_list_src.remove(file_list_des[i])
    if len(file_list_src) == 0:
        print("=====没有新文件需要压缩=======")
    compress('4', des_dir, src_dir, file_list_src)

def handle_photo():
    '''根据图片的文件名处理成需要的json格式的数据

    -----------
    最后将data.json文件存到博客的source/photos文件夹下
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    file_list = list_img_file(src_dir)
    list_info = []
    file_list.sort(key=lambda x: x.split('_')[0])   # 按照日期排序
    for i in range(len(file_list)):
        filename = file_list[i]
        date_str, info = filename.split("_")
        info, _ = info.split(".")
        # 更改：为加入月份未知或日期未知的图，更改日期的提取
        date_list = date_str.split("-")
        # print(date_list)
        assert len(date_list)==3
        # date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_str[0:7]  # 月份必须写成01月
        # 补充：图片尺寸
        img = Image.open(src_dir + filename)
        width = str(img.width)  # 图片的宽
        height = str(img.height)  # 图片的高

        if i == 0:  # 处理第一个文件
            new_dict = {"date": year_month, "arr":{'year': date_list[0],
                                                                'month': date_list[1],
                                                                'link': [filename],
                                                                'text': [info],
                                                                'type': ['image'],
                                                                'width': [width],
                                                                'height': [height],
                                                                   }
                                        }
            list_info.append(new_dict)
        elif year_month != list_info[-1]['date']:  # 不是最后的一个日期，就新建一个dict
            new_dict = {"date": year_month, "arr":{'year': date_list[0],
                                                   'month': date_list[1],
                                                   'link': [filename],
                                                   'text': [info],
                                                   'type': ['image'],
                                                   'width': [width],
                                                   'height': [height]
                                                   }
                        }
            list_info.append(new_dict)
        else:  # 同一个日期
            list_info[-1]['arr']['link'].append(filename)
            list_info[-1]['arr']['text'].append(info)
            list_info[-1]['arr']['type'].append('image')
            list_info[-1]['arr']['width'].append(width)
            list_info[-1]['arr']['height'].append(height)

    list_info.reverse()  # 翻转
    final_dict = {"list": list_info}
    with open("D:/Blog/liudeng129/blog/source/photos/data.json","w") as fp:
        json.dump(final_dict, fp)

def cut_photo():
    """裁剪算法

    ----------
    调用Graphics类中的裁剪算法，将src_dir目录下的文件进行裁剪（裁剪成正方形）
    """
    src_dir = "photos/"
    min_src_dir = "min_photos/"
    if directory_exists(src_dir):  # 若存在photos目录
        # 判断目录存在与否
        if not directory_exists(src_dir):
            make_directory(src_dir)  # 若目录不存在，新建一个
        if not directory_exists(min_src_dir):
            make_directory(min_src_dir)  # 若目录不存在，新建一个
        # business logic
        file_list = list_img_file(src_dir)  # 列出全部图片（jpg, png, gif）
        # print file_list
        if file_list:  # 如果图片列表不为空
            print_help()
            for infile in file_list:
                img = Image.open(src_dir+infile)  # 打开一张图片
                Graphics(infile=src_dir+infile, outfile=min_src_dir + infile).cut_by_ratio()
        else:
            pass
    else:
        print("source directory not exist!")

def clear_min():
    src_dir = "photos/"
    min_src_dir = "min_photos/"
    if directory_exists(src_dir):  # 若存在photos目录
        # 判断目录存在与否
        if not directory_exists(min_src_dir):
            make_directory(min_src_dir)  # 若min目录不存在，新建一个
        else:
            pass
        file_list = list_img_file(src_dir)  # 列出全部图片（jpg, png, gif）
        min_list = list_img_file(min_src_dir)
        # print file_list
        if min_list:  # 如果图片列表不为空
            for minfile in min_list:
                if minfile not in file_list:
                    print("发现一张已经清理的图！")
                    if os.path.isfile(min_src_dir + minfile):
                        os.remove(min_src_dir + minfile)
                        print("已经清理" + minfile)
                    else: print("未发现该缩略图")
    else:
        print("source directory not exist!")

def cut_and_compress():
    src_dir = "photos/"
    min_src_dir = "min_photos/"
    if directory_exists(src_dir):  # 若存在photos目录
        # 判断目录存在与否
        if not directory_exists(min_src_dir):
            make_directory(min_src_dir)  # 若min目录不存在，新建一个
        file_list = list_img_file(src_dir)  # 列出全部图片（jpg, png, gif）
        min_list = list_img_file(min_src_dir)
        if file_list:  # 如果图片列表不为空

            # file_list中，去除所有已经在min里的图
            for i in range(len(min_list)):
                if min_list[i] in file_list:
                    print("发现压缩过的图片："+min_list[i])
                    file_list.remove(min_list[i])

            # 切割图片
            for file in file_list:
                Graphics(infile=src_dir + file, outfile=min_src_dir + file).cut_by_ratio()

            if len(file_list) == 0:
                print("=====没有新文件需要压缩=======")
            else:
                compress('4', min_src_dir, src_dir, file_list)
    else:
        print("source directory not exist!")

def git_operation():
    '''
    git 命令行函数，将仓库提交

    ----------
    需要安装git命令行工具，并且添加到环境变量中
    '''
    os.system('git add --all')
    os.system('git commit -m "add photos"')
    os.system('git push origin')

if __name__ == "__main__":
    # cut_photo()        # 裁剪图片，裁剪成正方形，去中间部分
    # compress_photo()   # 压缩图片，并保存到mini_photos文件夹下
    clear_min()
    cut_and_compress()
    git_operation()    # 提交到github仓库
    handle_photo()     # 将文件处理成json格式，存到博客仓库中
    print("处理完成！下一步可以试试 hexo g！")
