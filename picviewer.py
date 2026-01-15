import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, 
                             QGraphicsView, QGraphicsScene, QVBoxLayout, 
                             QWidget, QPushButton, QToolBar, QColorDialog,
                             QSpinBox, QLabel, QHBoxLayout, QRubberBand)
from PySide6.QtGui import QPixmap, QPainter, QAction, QPen, QColor, QIcon, QCursor
from PySide6.QtCore import Qt, QRectF, QPoint, QRect, QSize

class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # 初始状态
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._pixmap_item = None
        self._original_pixmap = None  # 用于保存和绘图的底图
        self._source_pixmap = None    # 永久保存最初载入的图片，用于重置
        
        # 绘图与截图参数
        self.mode = "VIEW"  # VIEW, DRAW, CROP
        self.brush_color = QColor(Qt.red)
        self.brush_size = 5
        self.last_point = QPoint()
        
        # 截图辅助
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def load_image(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self._source_pixmap = pixmap
            # 使用 copy 确保编辑的是副本
            self._original_pixmap = pixmap.copy()
            self.refresh_scene()
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def reset_image(self):
        """恢复到最初加载的状态"""
        if self._source_pixmap:
            self._original_pixmap = self._source_pixmap.copy()
            self.refresh_scene()
            # 也可以选择是否重置视角，这里保持当前缩放还是恢复自适应？
            # 通常重置图片也会希望重置视角
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def refresh_scene(self):
        """将当前的 pixmap 更新到场景中"""
        if self._original_pixmap:
            self._scene.clear()
            self._pixmap_item = self._scene.addPixmap(self._original_pixmap)
            self._scene.setSceneRect(QRectF(self._original_pixmap.rect()))

    def set_mode(self, mode):
        self.mode = mode
        if mode == "VIEW":
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.setCursor(Qt.ArrowCursor)
        elif mode == "DRAW":
            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(Qt.CrossCursor)
        elif mode == "CROP":
            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(Qt.PrecisionCursor)

    def mousePressEvent(self, event):
        if self.mode == "DRAW" and event.button() == Qt.LeftButton:
            # 转换坐标到场景坐标
            self.last_point = self.mapToScene(event.pos()).toPoint()
        elif self.mode == "CROP" and event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == "DRAW" and event.buttons() & Qt.LeftButton:
            current_point = self.mapToScene(event.pos()).toPoint()
            self.draw_on_pixmap(self.last_point, current_point)
            self.last_point = current_point
        elif self.mode == "CROP" and self.rubber_band.isVisible():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mode == "CROP" and event.button() == Qt.LeftButton:
            rect = self.rubber_band.geometry()
            self.rubber_band.hide()
            self.crop_image(rect)
        else:
            super().mouseReleaseEvent(event)

    def draw_on_pixmap(self, p1, p2):
        """直接在底图 Pixmap 上绘画"""
        if self._original_pixmap:
            painter = QPainter(self._original_pixmap)
            pen = QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(p1, p2)
            painter.end()
            # 更新显示
            self._pixmap_item.setPixmap(self._original_pixmap)

    def crop_image(self, viewport_rect):
        """根据视图中的矩形进行截图/裁剪"""
        if not self._original_pixmap: return
        
        # 将视图坐标转换为场景坐标，再转换为图片像素坐标
        scene_rect = self.mapToScene(viewport_rect).boundingRect()
        image_rect = scene_rect.toRect().intersected(self._original_pixmap.rect())
        
        if not image_rect.isEmpty():
            cropped = self._original_pixmap.copy(image_rect)
            self._original_pixmap = cropped
            self.refresh_scene()
            self.set_mode("VIEW")

    def wheelEvent(self, event):
        if self.mode == "VIEW":
            zoom_in_factor = 1.25
            zoom_out_factor = 1 / zoom_in_factor
            if event.angleDelta().y() > 0:
                self.scale(zoom_in_factor, zoom_in_factor)
            else:
                self.scale(zoom_out_factor, zoom_out_factor)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PicViewerX - 图片浏览与简单编辑器")
        self.resize(1000, 660)

        self.viewer = ImageViewer()
        self.setCentralWidget(self.viewer)

        self.setup_ui()

    def setup_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 文件操作
        open_act = QAction("打开", self)
        open_act.triggered.connect(self.open_file)
        toolbar.addAction(open_act)

        save_act = QAction("另存为", self)
        save_act.triggered.connect(self.save_file)
        toolbar.addAction(save_act)
        

        
        toolbar.addSeparator()

        crop_act = QAction("裁剪", self)
        crop_act.triggered.connect(lambda: self.viewer.set_mode("CROP"))
        toolbar.addAction(crop_act)

        toolbar.addSeparator()       

        # 模式切换
        view_act = QAction("浏览", self)
        view_act.triggered.connect(lambda: self.viewer.set_mode("VIEW"))
        toolbar.addAction(view_act)

        toolbar.addSeparator()

        draw_act = QAction("标注", self)
        draw_act.triggered.connect(lambda: self.viewer.set_mode("DRAW"))
        toolbar.addAction(draw_act)

        toolbar.addSeparator()

        # 标注设置
        toolbar.addWidget(QLabel(" 颜色: "))
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(20, 20)
        self.color_btn.setStyleSheet("background-color: red; border: 1px solid gray;")
        self.color_btn.clicked.connect(self.choose_color)
        toolbar.addWidget(self.color_btn)

        toolbar.addWidget(QLabel(" 粗细: "))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 50)
        self.size_spin.setValue(5)
        self.size_spin.valueChanged.connect(self.change_size)
        toolbar.addWidget(self.size_spin)

        toolbar.addSeparator()

        # 重置功能
        reset_act = QAction("重置", self)
        reset_act.triggered.connect(self.viewer.reset_image)
        toolbar.addAction(reset_act)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if file_path:
            self.viewer.load_image(file_path)

    def save_file(self):
        if not self.viewer._original_pixmap:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "图片另存为", "result.png", "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        if file_path:
            self.viewer._original_pixmap.save(file_path)

    def choose_color(self):
        color = QColorDialog.getColor(self.viewer.brush_color, self)
        if color.isValid():
            self.viewer.brush_color = color
            self.color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")

    def change_size(self, val):
        self.viewer.brush_size = val

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())