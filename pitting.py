import os
import shutil
from collections import defaultdict


def rename_files(label_dir, data_dir, output_dir="renamed_files"):
    """
    参数说明:
    label_dir: label文件夹路径
    data_dir: data文件夹路径
    output_dir: 重命名后文件的输出目录 (默认为当前目录下的renamed_files文件夹)
    """
    # 创建输出目录
    os.makedirs(os.path.join(output_dir, "label"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "data"), exist_ok=True)

    # 获取label文件基本名（无扩展名）
    label_basenames = set()
    for filename in os.listdir(label_dir):
        if os.path.isfile(os.path.join(label_dir, filename)):
            basename = os.path.splitext(filename)[0]
            label_basenames.add(basename)

    # 匹配data文件夹中的文件
    matched_files = []
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if os.path.isfile(filepath):
            basename = os.path.splitext(filename)[0]
            if basename in label_basenames:
                matched_files.append((basename, filename))

    # 按文件名排序确保顺序一致
    matched_files.sort(key=lambda x: x[0])

    # 重命名并复制文件
    for idx, (basename, data_filename) in enumerate(matched_files, 1):
        # 新文件名格式：pitting_0001, pitting_0002...
        new_name = f"pitting_{idx:04d}"

        # 处理label文件
        label_files = [f for f in os.listdir(label_dir)
                       if f.startswith(basename) and os.path.isfile(os.path.join(label_dir, f))]

        for label_file in label_files:
            label_ext = os.path.splitext(label_file)[1]
            src_label = os.path.join(label_dir, label_file)
            dst_label = os.path.join(output_dir, "label", f"{new_name}{label_ext}")
            shutil.copy2(src_label, dst_label)

        # 处理data文件
        data_ext = os.path.splitext(data_filename)[1]
        src_data = os.path.join(data_dir, data_filename)
        dst_data = os.path.join(output_dir, "data", f"{new_name}{data_ext}")
        shutil.copy2(src_data, dst_data)

    print(f"操作完成！共处理 {len(matched_files)} 个文件对。")
    print(f"重命名后的文件保存在: {output_dir}")


# 使用示例
if __name__ == "__main__":
    label_folder = r"F:\reproduce\UNet_Demo\BSData-main\label"  # 替换为实际路径
    data_folder = r"F:\reproduce\UNet_Demo\BSData-main\data"  # 替换为实际路径

    rename_files(label_folder, data_folder)