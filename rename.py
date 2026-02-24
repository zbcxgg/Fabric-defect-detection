import os


def add_prefix_to_images(folder_path):
    # 获取文件夹名称作为前缀
    folder_name = os.path.basename(folder_path)

    # 支持的图片格式扩展名
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 获取文件扩展名
        ext = os.path.splitext(filename)[1].lower()

        # 只处理图片文件
        if ext in image_extensions:
            # 构造新文件名
            new_name = f"{folder_name}_{filename}"

            # 原始文件完整路径
            old_path = os.path.join(folder_path, filename)
            # 新文件完整路径
            new_path = os.path.join(folder_path, new_name)

            # 重命名文件
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")


if __name__ == "__main__":
    # 使用示例（修改为你的文件夹路径）
    target_folder = r"F:\reproduce\UNet_Demo\VOCdevkit\VOC2007\misplaced"

    # 执行重命名
    add_prefix_to_images(target_folder)
    print("All images have been renamed!")