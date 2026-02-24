import os
from PIL import Image
import numpy as np
def convert_masks(input_folder, output_folder, background_value=0, target_value=1, target_labels=None):
    # 如果目标标签列表为空，则假设所有非背景标签都是目标
    if target_labels is None:
        def is_target(label):
            return label != background_value
    else:
        def is_target(label):
            return label in target_labels
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 构建完整的文件路径
        file_path = os.path.join(input_folder, filename)
        # 检查文件是否是图像（根据扩展名）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            try:
                # 打开图像
                with Image.open(file_path) as img:
                    # 转换图像为可修改的像素数组
                    pixels = np.array(img)

                    # 如果图像是灰度图（单通道），直接处理
                    if len(pixels.shape) == 2:
                        binary_pixels = (pixels == background_value).astype(np.uint8) * 0 + (
                                    pixels != background_value).astype(np.uint8) * 1
                    # 如果图像是多通道（例如RGB），但mask应该是单通道的，所以这里可能需要额外处理
                    # 但对于标准的mask图像，这通常不会发生，所以我们假设是单通道
                    else:
                        raise ValueError(
                            "Unexpected mask image format: expected single channel (grayscale), but got {}".format(
                                pixels.shape))

                    # 如果需要基于特定的目标标签列表来处理
                    # 注意：这个部分在标准二分类中通常不需要，因为只区分背景和目标
                    # 但为了完整性，我还是保留了这部分代码
                    # if len(pixels.shape) == 2 and target_labels is not None:
                    #     binary_pixels = ((pixels == np.array(list(target_labels), dtype=np.uint8)).any(axis=-1)).astype(np.uint8)

                    # 但实际上，对于二分类，我们只需要上面的简单判断即可

                    # 将修改后的像素数组转换回图像
                    binary_img = Image.fromarray(binary_pixels)

                    # 构建输出文件路径
                    output_path = os.path.join(output_folder, filename)

                    # 保存二值化后的图像
                    binary_img.save(output_path)
                    print(f"Processed and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


# 注意：上面的代码中有一个关于多通道处理的警告，但实际上对于mask图像，这通常不会发生
# 因为mask图像通常是单通道的灰度图。如果确实遇到了多通道图像，请检查你的数据集

# 指定输入和输出文件夹路径
input_folder_path = r'F:\reproduce\UNet_Demo\VOCdevkit1\VOC2007\SegmentationClass1'  # 替换为你的输入mask文件夹路径
output_folder_path = r'F:\reproduce\UNet_Demo\VOCdevkit1\VOC2007\SegmentationClass'  # 替换为你的输出文件夹路径

# 调用函数执行转换操作
# 在这个例子中，我们没有特定的目标标签列表，所以传递None，并使用默认的背景值0
convert_masks(input_folder_path, output_folder_path, background_value=0, target_labels=None)