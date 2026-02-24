import os
import shutil


def delete_jpg_files(folder_path):
    # 遍历指定文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件是否为.jpg格式
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                try:
                    # 删除文件
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")


if __name__ == "__main__":
    # 指定文件夹路径
    folder_to_clean = r"F:\reproduce\UNet_Demo\VOCdevkit\VOC2007\SegmentationClass"  # 替换为你的文件夹路径
    delete_jpg_files(folder_to_clean)