import os
import numpy as np
from PIL import Image

from unet import Unet
# from utils.utils_metrics import compute_single_mIoU  # 需要自定义单张图片计算函数

'''
单张图片 mIoU 计算代码
注意：需要先实现 compute_single_mIoU 函数（见下方说明）
'''


def compute_single_mIoU(gt_image, pred_image, num_classes, name_classes):
    """
    计算单张图片的 mIoU 及其他指标
    参数:
        gt_image: PIL Image 格式的真实标签（灰度图，像素值为类别索引）
        pred_image: PIL Image 格式的预测结果（灰度图，像素值为类别索引）
        num_classes: 类别数（含背景）
        name_classes: 类别名称列表
    返回:
        hist: 混淆矩阵
        IoUs: 各类别 IoU
        PA_Recall: 各类别召回率
        Precision: 各类别精确率
    """
    # 将图像转换为 numpy 数组
    gt = np.array(gt_image)
    pred = np.array(pred_image)

    # 确保预测图和真实图尺寸一致
    assert gt.shape == pred.shape, "预测图与真实图尺寸不一致"

    # 初始化混淆矩阵（num_classes x num_classes）
    hist = np.zeros((num_classes, num_classes))

    # 统计每个像素的类别关系
    mask = (gt >= 0) & (gt < num_classes)
    hist = np.bincount(
        num_classes * gt[mask].astype(int) + pred[mask],
        minlength=num_classes ** 2
    ).reshape(num_classes, num_classes)

    # 计算 IoU
    IoUs = np.diag(hist) / (hist.sum(1) + hist.sum(0) - np.diag(hist) + 1e-10)

    # 计算召回率 (Recall)
    PA_Recall = np.diag(hist) / (hist.sum(1) + 1e-10)

    # 计算精确率 (Precision)
    Precision = np.diag(hist) / (hist.sum(0) + 1e-10)

    return hist, IoUs, PA_Recall, Precision


if __name__ == "__main__":
    # 参数设置
    num_classes = 2
    name_classes = ["background", "detect"]

    # 图片路径（请修改为你的实际路径）
    image_path = r"F:\reproduce\UNet_Demo\分割效果-RPC\原图\3.jpg"
    gt_path = r"F:\reproduce\UNet_Demo\分割效果-RPC\灰度\3.png"  # 真实标签图（灰度）

    # 加载模型
    unet = Unet()

    # 预测单张图片
    image = Image.open(image_path)
    pred_image = unet.get_miou_png(image)  # 获取预测结果（灰度图）

    # 加载真实标签
    gt_image = Image.open(gt_path)

    # 计算指标
    hist, IoUs, PA_Recall, Precision = compute_single_mIoU(gt_image, pred_image, num_classes, name_classes)

    # 计算平均指标（忽略NaN值）
    miou = np.nanmean(IoUs)  # 平均IoU
    mprecision = np.nanmean(Precision)  # 平均Precision
    mrecall = np.nanmean(PA_Recall)  # 平均Recall

    # 打印结果
    print("===== 单张图片评估结果 =====")
    for i in range(num_classes):
        print(f"{name_classes[i]}: IoU = {IoUs[i]:.4f}, Recall = {PA_Recall[i]:.4f}, Precision = {Precision[i]:.4f}")

    print("\n===== 平均指标 =====")
    print(f"mIoU = {miou:.4f}")
    print(f"mPrecision = {mprecision:.4f}")
    print(f"mRecall = {mrecall:.4f}")

    # 可选：计算F1分数（Precision和Recall的调和平均）
    f1_score = 2 * (mprecision * mrecall) / (mprecision + mrecall + 1e-10)
    print(f"F1-Score = {f1_score:.4f}")