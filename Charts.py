from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt


class HPBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.__painter = QtGui.QPainter(self)

        self.__pen_border = QtGui.QPen(QtGui.QColor(127, 127, 127), 2, Qt.PenStyle.SolidLine)
        self.__pen_none = QtGui.QPen(Qt.PenStyle.NoPen)
        self.__pen_text = QtGui.QPen(QtGui.QColor(0, 0, 0), 12)

        self.__brush_border = QtGui.QBrush(Qt.BrushStyle.NoBrush)
        self.__brush_fill = QtGui.QBrush(QtGui.QColor(127, 255, 255))
        self.__brush_mask = QtGui.QBrush(QtGui.QColor(127, 127, 255), Qt.BrushStyle.Dense3Pattern)

        self.__brush_background = QtGui.QBrush(QtGui.QColor(255, 255, 255))

        self.__rect_border = QtCore.QRect(2, 2, 335, 35)
        self.__rect_fill = QtCore.QRect(3, 3, 166, 33)
        self.__rect_mask = QtCore.QRect(3, 3, 0, 0)
        self.__rect_background = QtCore.QRect(3, 3, 333, 33)

        self.__rect_text = QtCore.QRect()

        self.__text = "50/100"

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.__painter.begin(self)
        self.__painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.Antialiasing)

        self.__painter.setPen(self.__pen_none)
        self.__painter.setBrush(self.__brush_background)
        self.__painter.drawRect(self.__rect_background)

        self.__painter.setPen(self.__pen_none)
        self.__painter.setBrush(self.__brush_mask)
        self.__painter.drawRect(self.__rect_mask)

        self.__painter.setPen(self.__pen_none)
        self.__painter.setBrush(self.__brush_fill)
        self.__painter.drawRect(self.__rect_fill)

        self.__painter.setPen(self.__pen_border)
        self.__painter.setBrush(self.__brush_border)
        self.__painter.drawRoundedRect(self.__rect_border, 5, 5)

        self.__rect_text.setRect(0, 0, self.width(), self.height() - 5)

        self.__painter.setPen(self.__pen_text)
        self.__painter.drawText(self.__rect_text,
                                QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
                                self.__text)
        self.__painter.end()

    def set_value(self, total, value, mask=0):
        self.__text = f"{value} / {total}"
        self.__rect_fill.setRect(3, 3, 333 * (value / total), 33)
        self.__rect_mask.setRect(3, 3, 333 * ((value + mask) / total), 33)
        ...

    def set_color(self, fill=(127, 255, 255), mask=(127, 127, 255), background=(255, 255, 255)):
        self.__brush_fill.setColor(QtGui.QColor(*fill))
        self.__brush_mask.setColor(QtGui.QColor(*mask))
        self.__brush_background.setColor((QtGui.QColor(*background)))
        self.repaint()

    def clear(self):
        self.__painter.eraseRect(0, 0, self.width(), self.height())
