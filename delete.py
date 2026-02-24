import os
import shutil


def retain_matching_prefixes(folder_a, folder_b):
    # 获取A文件夹中所有图片文件的前缀集合
    prefixes_a = set()
    for filename in os.listdir(folder_a):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):  # 可根据需要添加更多扩展名
            prefix = filename.split('.')[0]
            prefixes_a.add(prefix)

    # 遍历B文件夹，删除不匹配前缀的图片文件
    for filename in os.listdir(folder_b):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):  # 同样，根据需要添加扩展名
            prefix = filename.split('.')[0]
            if prefix not in prefixes_a:
                file_path = os.path.join(folder_b, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")


# 指定文件夹路径
folder_a_path = r'E:\reproduce\UNet_Demo\VOCdevkit\VOC2007\JPEGImages'  # 替换为你的A文件夹路径
folder_b_path = r'E:\reproduce\UNet_Demo\VOCdevkit\VOC2007\SegmentationClass' # 替换为你的B文件夹路径

# 调用函数执行操作
retain_matching_prefixes(folder_a_path, folder_b_path)


