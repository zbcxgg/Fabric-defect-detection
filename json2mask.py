import os
import json
import numpy as np
import cv2
from tqdm import tqdm


def json_to_mask(json_path, output_dir):
    """
    将JSON标注文件转换为PNG掩码图像
    :param json_path: JSON文件路径
    :param output_dir: 掩码输出目录
    """
    # 读取JSON数据
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 获取图像尺寸
    height = data['imageHeight']
    width = data['imageWidth']

    # 创建全黑掩码
    mask = np.zeros((height, width), dtype=np.uint8)

    # 遍历所有形状标注
    for shape in data['shapes']:
        if shape['shape_type'] == 'polygon':
            # 提取多边形点并转换为整数坐标
            points = np.array(shape['points'], dtype=np.int32)

            # 在掩码上绘制填充多边形（白色）
            cv2.fillPoly(mask, [points], color=255)

    # 创建输出路径
    filename = os.path.basename(json_path).replace('.json', '.png')
    output_path = os.path.join(output_dir, filename)

    # 保存掩码图像
    cv2.imwrite(output_path, mask)


def process_label_folder(label_dir, output_dir):
    """
    处理整个标签文件夹
    :param label_dir: JSON标签文件夹路径
    :param output_dir: 掩码输出文件夹路径
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有JSON文件
    json_files = [f for f in os.listdir(label_dir) if f.endswith('.json')]

    # 进度条处理
    for filename in tqdm(json_files, desc='Processing masks'):
        json_path = os.path.join(label_dir, filename)
        json_to_mask(json_path, output_dir)


if __name__ == "__main__":
    # 配置路径
    LABEL_DIR = r'F:\reproduce\UNet_Demo\renamed_files\label'  # JSON标签文件夹
    MASK_DIR = r'F:\reproduce\UNet_Demo\renamed_files\mask'  # 掩码输出文件夹

    # 执行转换
    process_label_folder(LABEL_DIR, MASK_DIR)
    print(f"转换完成！掩码已保存至: {MASK_DIR}")