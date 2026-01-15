# PicViewer - 极简看图与标注工具 
# Minimalist Image Viewer & Annotation Tool

## 基于 Python 和 PySide6 开发的轻量级桌面看图工具，集成了基础查看、截图裁剪与画笔标注功能。
## A lightweight desktop image viewer built with Python and PySide6, featuring basic viewing, cropping, and brush annotation capabilities.

# 功能特性 
# Features

## 基础查看 
## Basic Viewing:

- 支持常用格式（JPG, PNG, BMP, WebP）。
- Supports common formats (JPG, PNG, BMP, WebP).

- 丝滑的缩放（鼠标滚轮）与平移（鼠标拖拽）。
- Smooth zooming (mouse wheel) and panning (mouse drag).

- 自动适应窗口大小。
- Automatic fit-to-window scaling.

## 截图与裁剪 / Screenshot & Crop:

- 可视化拉框选择区域。
- Visual rectangle selection.

- 一键裁剪并实时更新。
- Instant crop and live update.

## 标注功能 
## Annotation:

- 自由画笔涂鸦。
- Freehand brush drawing.

- 自定义颜色与粗细。
- Customizable brush color and thickness.

## 管理操作 
## Management:

- 重置 (Reset): 随时撤销所有修改，恢复到原始图片状态。
- Revert all changes and restore the original image at any time.

- 另存为 (Save As): 将修改后的图片导出为新文件。
- Export modified images as new files.

# 安装要求 
# Prerequisites

## 确保你的系统中已安装 Python 3.x。
## Ensure Python 3.x is installed on your system.

## 依赖库安装 
## Install Dependencies

唯一需要的第三方库是 PySide6：
The only third-party dependency is PySide6:

```Shell
pip install PySide6
```

# 运行指南 / How to Run

## 下载或复制代码到本地并保存为 PicViewer.py。
## Download or copy the code to your local machine as PicViewer.py.

## 在终端运行：
## Run in your terminal:

```Shell
python viewer.py
```

# 使用指南 / Usage Guide

## 打开图片 (Open): 点击工具栏“打开”选择图片。
## Click "Open" to select an image.

## 模式切换 (Modes):

- 浏览 (View): 默认模式，可拖拽和缩放。
- Default mode, allows panning and zooming.

- 裁剪 (Crop): 在图上拉出一个矩形，松开后即可完成裁剪。
- Drag a rectangle on the image and release to crop.

- 标注 (Draw): 使用画笔在图上直接绘画。
- Use the brush to draw directly on the image.

- 自定义 (Customize): 在标注模式下，点击颜色块更改颜色，调整数值更改画笔粗细。
- In Draw mode, click the color block to change color and adjust the spin box for brush thickness.

- 重置 (Reset): 如果不满意当前修改，点击“重置”即可。
- Click "Reset" if you are not satisfied with current modifications.

# 打包发布 / Packaging

## 你可以使用 PyInstaller 将其打包成独立的 .exe (Windows) 或可执行文件：
## You can use PyInstaller to bundle it into a standalone executable:

```Shell
pip install pyinstaller
```
```Shell
pyinstaller --noconsole --onefile PicViewer.py
```


## 打包后的PicViewer.exe文件将出现在 dist 文件夹中。
## The output PicViewer.exe file will be located in the dist folder.

# 开源协议 / License

本项目采用 MIT 协议。你可以自由地修改和分发。
This project is licensed under the MIT License. Feel free to modify and distribute.
