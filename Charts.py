from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt


class HPBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.__painter = QtGui.QPainter(self)

        self.__pen_border = QtGui.QPen(QtGui.QColor(127, 127, 127), 2, Qt.PenStyle.SolidLine)
        self.__brush_border = QtGui.QBrush(Qt.BrushStyle.NoBrush)

        self.__pen_fill_mask = QtGui.QPen(Qt.PenStyle.NoPen)
        self.__brush_fill = QtGui.QBrush(QtGui.QColor(127, 255, 255))

        self.__pen_mask = QtGui.QPen(QtGui.QColor(127, 127, 127), 1, Qt.PenStyle.NoPen)

        self.__border = QtCore.QRect(4, 4, 335, 35)
        self.__fill_rect = QtCore.QRect(5, 5, 189, 33)
        self.__mask_rect = QtCore.QRect(5, 5, 5, 5)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.__painter.begin(self)
        self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.Antialiasing)

        self.__painter.setPen(self.__pen_fill_mask)
        self.__painter.setBrush(self.__brush_fill)
        self.__painter.drawRect(self.__fill_rect)

        self.__painter.setPen(self.__pen_border)
        self.__painter.setBrush(self.__brush_border)
        self.__painter.drawRoundedRect(self.__border, 5, 5)
        self.__painter.end()

    def set(self):
        self.__painter.setPen(self.__pen_border)
        self.__fill_rect.setRect(5, 5, 189, 33)  # 改变长方形大小
        self.repaint()
