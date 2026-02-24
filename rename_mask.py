import os


def clean_and_rename_images(folder_path):
    try:
        # 标准化路径并验证有效性
        folder_path = os.path.normpath(folder_path)
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"路径不存在: {folder_path}")

        # 获取文件夹名称作为前缀
        folder_name = os.path.basename(folder_path)

        # 支持的图片格式扩展名（可扩展）
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif',
                            '.bmp', '.tiff', '.webp', '.svg']

        # 遍历文件夹内容
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 跳过子目录和非文件项
            if not os.path.isfile(file_path):
                continue

            # 分割文件名和扩展名
            name_part, ext = os.path.splitext(filename)
            ext = ext.lower()  # 统一小写处理

            # 仅处理图片文件
            if ext in image_extensions:
                # 清理文件名：移除所有'_mask'出现
                cleaned_name = name_part.replace('_mask', '')

                # 构建新文件名
                new_filename = f"{folder_name}_{cleaned_name}{ext}"
                new_path = os.path.join(folder_path, new_filename)

                # 防重复处理
                if os.path.exists(new_path):
                    print(f"⚠️ 跳过：{new_filename} 已存在")
                    continue

                # 执行重命名
                os.rename(file_path, new_path)
                print(f"✅ 已重命名：{filename} → {new_filename}")

    except Exception as e:
        print(f"❌ 操作失败：{str(e)}")


if __name__ == "__main__":
    # 配置路径（使用原始字符串）
    target_folder = r"F:\reproduce\UNet_Demo\VOCdevkit\VOC2007\misplaced"

    # 交互式输入路径（可选）
    # target_folder = input("请输入图片文件夹路径：").strip()

    clean_and_rename_images(target_folder)
    print("🎉 处理完成！")