import os
from PIL import Image


def convert_and_clean(folder_path, quality=90, remove_png=True):
    """
    PNG转JPG并清理原文件

    参数：
    folder_path - 目标文件夹路径
    quality - JPG保存质量 (1-100)
    remove_png - 是否删除原始PNG文件
    """
    converted = []
    failed = []
    existing_jpg = []

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        # 只处理PNG文件
        if not filename.lower().endswith('.png'):
            if filename.lower().endswith('.jpg'):
                existing_jpg.append(filename)
            continue

        # 生成唯一JPG文件名
        base_name = os.path.splitext(filename)[0]
        jpg_filename = generate_unique_name(folder_path, base_name)
        jpg_path = os.path.join(folder_path, jpg_filename)

        try:
            # 打开并转换图片
            with Image.open(full_path) as img:
                # 处理透明背景
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # 保存高质量JPG
                img.save(jpg_path, 'JPEG', quality=quality, optimize=True)
                converted.append(filename)

                # 安全删除PNG
                if remove_png:
                    os.remove(full_path)
                    print(f"✓ 转换成功并删除: {filename} → {jpg_filename}")
                else:
                    print(f"✓ 转换成功: {filename} → {jpg_filename}")

        except Exception as e:
            failed.append(filename)
            print(f"× 转换失败 {filename}: {str(e)}")

    # 输出统计报告
    print("\n===== 转换报告 =====")
    print(f"成功转换: {len(converted)} 个PNG文件")
    print(f"失败文件: {len(failed)} 个")
    print(f"已有JPG文件: {len(existing_jpg)} 个")

    if failed:
        print("\n失败列表:")
        for f in failed:
            print(f"  - {f}")


def generate_unique_name(folder, base_name):
    """生成不重复的JPG文件名"""
    counter = 0
    while True:
        suffix = f"_{counter}" if counter > 0 else ""
        candidate = f"{base_name}{suffix}.jpg"
        if not os.path.exists(os.path.join(folder, candidate)):
            return candidate
        counter += 1


if __name__ == "__main__":
    # 使用示例（修改路径）
    target_folder = r"F:\reproduce\UNet_Demo\VOCdevkit\VOC2007\JPEGImages"

    # 验证路径
    if not os.path.isdir(target_folder):
        print(f"错误：文件夹路径不存在 - {target_folder}")
        exit()

    # 执行转换（质量85，删除原始PNG）
    convert_and_clean(target_folder, quality=85, remove_png=True)