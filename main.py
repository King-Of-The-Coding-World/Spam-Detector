import sys
import math
from spamDetector import checkStatus
from about import AboutDialog

from PySide6.QtWidgets import (
    QPushButton, QLabel, QPlainTextEdit, QApplication, QMainWindow, QSlider)

from PySide6.QtCore import (
    Qt, QTimer, Property, QPointF, QPropertyAnimation, QParallelAnimationGroup,
    Signal, QSize, QRect, QUrl)

from PySide6.QtGui import (
    QColor, QPainter, QPen, QPainterPath, QBrush, QFont, QFontDatabase)

from PySide6.QtMultimedia import (QMediaPlayer, QSoundEffect, QAudioOutput)


class titleBar(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.oldPos = None
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("QLabel{background: transparent;}")

        # Our font to write 'Spam Detector'
        self.fontID1 = QFontDatabase.addApplicationFont(
            "./assets/fonts/Beautiful ES.ttf")
        self.beautifulES = QFont(
            QFontDatabase.applicationFontFamilies(self.fontID1), 34)
        self.beautifulES.setWeight(QFont.Weight.Medium)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Creating Printer Body
        printerPen = QPen()
        printerPen.setColor(QColor("#98A6A4"))
        printerPen.setWidth(3)

        painter.setPen(printerPen)
        painter.setBrush(QColor("#D3F4FF"))

        a = 25

        r = 10  # radius
        w = self.width()
        h = self.height() - a
        path = QPainterPath()

        # Start at top-left corner (after curve)
        path.moveTo(r, 0)

        # Top line
        path.lineTo(w - r, 0)

        # 1st curve
        path.arcTo(w - 2*r, 0, 2*r, 2*r, 90, -90)

        # right line 1
        path.lineTo(w, r + 15)

        # 2nd curve
        path.arcTo(w - 2*r, 15, 2*r, 2*r, 0, -90)

        # bottom line 1
        path.lineTo(w - 330, 35)

        # 3rd curve
        path.arcTo(w - 330 - r, 35, 2*r, 2*r, 90, 90)

        # right line 2
        path.lineTo(w - 330 - r, h - r)

        # 4th curve
        path.arcTo(w - 330 - 3*r, h - 2*r, 2*r, 2*r, 0, -90)

        # bottom line 2
        path.lineTo(r, h)

        # 5th curve
        path.arcTo(0, h - 2*r, 2*r, 2*r, 270, -90)

        # left line
        path.lineTo(0, r)

        # 6th and final curve
        path.arcTo(0, 0, 2*r, 2*r, 180, -90)

        path.closeSubpath()
        painter.drawPath(path)

    # Drawing the underShape
        painter.setBrush("#A8DCEB")
        underShape = QPainterPath()
        underShape.moveTo(0, h-r)
        underShape.lineTo(0, h+a-r)
        underShape.arcTo(0, h+a-2*r, 2*r, 2*r, 180, 90)
        underShape.lineTo(w-330-2*r, h+a)
        underShape.arcTo(w-330-3*r, h+a-2*r, 2*r, 2*r, 270, 90)
        underShape.lineTo(w-330-r, h-r)
        underShape.arcTo(w-330-3*r, h-2*r, 2*r, 2*r, 0, -90)
        underShape.lineTo(r, h)
        underShape.arcTo(0, h - 2*r, 2*r, 2*r, 270, -90)
        underShape.closeSubpath()
        painter.drawPath(underShape)

        underShapeBig = QPainterPath()
        underShapeBig.moveTo(w - 330, r+25)
        underShapeBig.lineTo(w-2*r, r+25)
        underShapeBig.arcTo(w-2*r, r+5, 2*r, 2*r, 270, 90)
        underShapeBig.lineTo(w, a+2*r)
        underShapeBig.arcTo(w-2*r, a+r, 2*r, 2*r, 0, -90)
        underShapeBig.lineTo(w - 330, a+3*r)
        underShapeBig.arcTo(w - 330 - r, a+3*r, 2*r, 2*r, 90, 90)
        underShapeBig.lineTo(w - 330 - r, r+35)
        underShapeBig.arcTo(w - 330 - r, r+25, 2*r, 2*r, 180, -90)

        painter.drawPath(underShapeBig)

    # Drawing the steel plate on the printer
        painter.setBrush("#E5F5FA")
        painter.setPen("#95BCCB")
        painter.drawRoundedRect(20, 35, 220, 70, 10, 10)

    # Writing 'Spam Detector'
        painter.setPen("#95BCCB")
        painter.setFont(self.beautifulES)

        painter.drawText(30, 60, "Spam")
        painter.drawText(80, 90, "Detector")

    # Drawing Stars
        painter.setPen("#E5F5FA")
        painter.setBrush("#95BCCB")

        def drawStar(center, radius, rotation=0):
            starPath = QPainterPath()
            starPath.setFillRule(Qt.FillRule.WindingFill)
            points = []

            for i in range(5):
                angle = math.radians(i * 72 - 90 + rotation)
                x = center.x() + radius * math.cos(angle)
                y = center.y() + radius * math.sin(angle)
                points.append(QPointF(x, y))

            order = [0, 2, 4, 1, 3]

            starPath.moveTo(points[order[0]])
            for j in range(1, 5):
                starPath.lineTo(points[order[j]])

            starPath.closeSubpath()
            painter.drawPath(starPath)

        def placeStars(center, radius, starRadiusList, extraAngle, rotation=0):
            points = []

            for i in range(len(starRadiusList)):
                angle = math.radians(i * 15 - 90 + rotation)
                x = center.x() + radius * math.cos(angle)
                y = center.y() + radius * math.sin(angle)

                points.append(QPointF(x, y))

            for j in range(len(starRadiusList)):
                drawStar(points[j], starRadiusList[j],
                         j * 18 + extraAngle)

        # Placing the stars
        placeStars(QPointF(150, 116), 70, [8, 9, 10, 9, 8], 0, 10)
        placeStars(QPointF(150, 116), 70, [8, 9, 10, 9, 8], 36, 10)

    # Drawing the bottom-left and top-right fillers of steel plate
        fillerBrush = QBrush("#95BCCB")
        fillerBrush.setStyle(Qt.BrushStyle.Dense4Pattern)

        painter.setPen("#95BCCB")
        painter.setBrush(fillerBrush)

        TfillerPath = QPainterPath()
        TfillerPath.moveTo(160, 35)
        TfillerPath.lineTo(230, 35)
        TfillerPath.arcTo(220, 35, 20, 20, 90, -90)
        TfillerPath.lineTo(240, 95)
        TfillerPath.arcTo(220, 85, 20, 20, 0, -90)
        TfillerPath.arcTo(90, 35, 140, 140, 0, 90)
        TfillerPath.closeSubpath()

        BfillerPath = QPainterPath()
        BfillerPath.moveTo(20, 65)
        BfillerPath.lineTo(20, 95)
        BfillerPath.arcTo(20, 85, 20, 20, 180, 90)
        BfillerPath.lineTo(60, 105)
        BfillerPath.arcTo(20, 25, 80, 80, 270, -90)
        BfillerPath.closeSubpath()

        painter.drawPath(TfillerPath)
        painter.drawPath(BfillerPath)

    # Drawing the Paper's input slot
        painter.setBrush("#FFFFFF")
        painter.setPen(QPen(QColor("#95BCCB"), 5))

        painter.drawRoundedRect(20, 15, 220, 10, 5, 5)

    # Drawing the Paper's output slot
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush("#E7E4E4")

        painter.drawRect(15, h+10, 230, 5)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.oldPos = ev.globalPosition().toPoint(
            ) - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, ev):
        if ev.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(ev.globalPosition().toPoint() - self.oldPos)


class Paper(QLabel):

    # Creating Signals. We always create them outside to avoid making raw signal objects.
    disableButtonSignal = Signal()
    enableButtonSignal = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("QLabel{background: transparent}")

        self.paperMargin = 10  # Ends of line will be this much far from left and right curve

        # to get the x coord of curves at a particular y of line
        self.xofLeft = lambda y: 10 - math.sqrt(100 - (y*y/100))  # for left
        self.xofRight = lambda y: 10 + math.sqrt(100 - (y*y/100))  # for right

        # Defining Animation
        self._offset = -100.0
        self.paperInDuration = 1200

        self.xAnim = QPropertyAnimation(self, b"offset")
        self.xAnim.setStartValue(-100.0)
        self.xAnim.setEndValue(0)
        self.xAnim.setDuration(self.paperInDuration)
        self.xAnim.setLoopCount(2)
        self.xAnim.finished.connect(self.enableButtonSignal.emit)

    # Property
    def getOffSet(self):
        return self._offset

    def setOffSet(self, value):
        self._offset = value
        self.update()

    offset = Property(float, getOffSet, setOffSet)

    # trigger function and sending disable signal
    def comeOut(self):
        self.disableButtonSignal.emit()
        self.xAnim.start()

    # The paintEvent
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen("#888888")
        painter.setBrush("#FFFFFF")

        # Drawing the body of paper
        r, w, h = 10, self.width(), self.height()

        paperPath = QPainterPath()
        paperPath.moveTo(0, 0)
        paperPath.lineTo(self.width(), 0)
        paperPath.arcTo(w - 2*r, -h, 2*r, 2*h, 0, -90)
        paperPath.lineTo(20, 100)
        paperPath.arcTo(0, -h, 2*r, 2*h, 270, -90)

        paperPath.closeSubpath()
        painter.drawPath(paperPath)

        # Drawing the lines.
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        painter.save()

        painter.setPen("#888888")
        for i in range(10):
            y = self.offset + 20*i
            painter.drawLine(QPointF(self.xofLeft(10 if y > 100 else y) + self.paperMargin, y),
                             QPointF(self.xofRight(10 if y > 100 else y) + 200 - self.paperMargin, y))

        painter.setPen("#FFFFFF")
        painter.drawLine(10, 100, 210, 100)
        painter.drawLine(0, 0, 220, 0)

        painter.restore()


class checkBtn(QPushButton):
    def __init__(self, btnText, parent=None):
        super().__init__(parent)
        self.btnText = btnText
        self.showUnderShape = True

    def setBtnText(self, value):
        self.btnText = value

    def setIn(self, value: bool):
        self.showUnderShape = value
        if not self.showUnderShape:
            self.move(self.x(), self.y() + 10)
        else:
            self.move(self.x(), self.y() - 10)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen("#FFA673")
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush("#561B06")

        # Drawing the Body
        r, w, h = 10, self.width(), self.height() - 15
        coordsBody = [QPointF(w-r, 0), QPointF(w, r), QPointF(w, h-r),
                      QPointF(w-r, h), QPointF(r, h), QPointF(0, h-r), QPointF(0, r)]
        buttonShape = QPainterPath()
        buttonShape.moveTo(r, 0)
        for i in coordsBody:
            buttonShape.lineTo(i)

        buttonShape.closeSubpath()
        painter.drawPath(buttonShape)

        # Drawing the Design
        coordsOuterLine = [QPointF(w-2*r, r), QPointF(w-r, 2*r), QPointF(w-r, h-2*r),
                           QPointF(w-2*r, h-r), QPointF(2*r, h-r), QPointF(r, h-2*r), QPointF(r, 2*r)]
        coordsInnerLine = [QPointF(w-2*r-5, r+5), QPointF(w-r-5, 2*r+5), QPointF(w-r-5, h-2*r-5),
                           QPointF(w-2*r-5, h-r-5), QPointF(2*r+5, h-r-5), QPointF(r+5, h-2*r-5), QPointF(r+5, 2*r+5)]

        outerLinePath = QPainterPath()
        outerLinePath.moveTo(2*r, r)
        innerLinePath = QPainterPath()
        innerLinePath.moveTo(2*r+5, r+5)

        for j in coordsOuterLine:
            outerLinePath.lineTo(j)
        for k in coordsInnerLine:
            innerLinePath.lineTo(k)

        outerLinePath.closeSubpath()
        innerLinePath.closeSubpath()

        framePath = QPainterPath()
        framePath.setFillRule(Qt.FillRule.OddEvenFill)
        framePath.addPath(outerLinePath)
        framePath.addPath(innerLinePath)

        painter.setBrush(QBrush("#FFA673", Qt.BrushStyle.Dense4Pattern))
        painter.drawPath(framePath)

        # Drawing the Text
        # Our font to write 'Spam Detector'
        self.fontID1 = QFontDatabase.addApplicationFont(
            "./assets/fonts/Cinzel-Bold.otf")
        self.Cinzel = QFont(
            QFontDatabase.applicationFontFamilies(self.fontID1), 16)
        self.Cinzel.setWeight(QFont.Weight.Bold)

        self.Cinzel.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
        painter.setFont(self.Cinzel)
        painter.drawText(self.rect().adjusted(0, -6, 0, -6),
                         Qt.AlignmentFlag.AlignCenter, self.btnText)

        # Drawing and writing the button press logic
        innerShape = QPainterPath()
        innerShape.moveTo(0, h-r)
        innerShape.lineTo(r, h)
        innerShape.lineTo(w-r, h)
        innerShape.lineTo(w, h-r)
        innerShape.lineTo(w, h)
        innerShape.lineTo(w-r, h+10)
        innerShape.lineTo(r, h+10)
        innerShape.lineTo(0, h)
        innerShape.closeSubpath()

        if self.showUnderShape:
            painter.drawPath(innerShape)
            painter.setPen(QPen(QColor("#561B06"), 2))

            painter.drawLines([QPointF(0, h-r), QPointF(0, h), QPointF(0, h),
                               QPointF(r, h+10), QPointF(r, h + 10),
                               QPointF(w-r, h+10), QPointF(w-r, h+10),
                               QPointF(w, h), QPointF(w, h-r), QPointF(w, h)])
            painter.drawLine(r, h-2, r, h+10)
            painter.drawLine(w-r, h-2, w-r, h+10)


class settingsPanel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen("#561B06")
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush("#FFA673")

        # Drawing the Body
        r, w, h = 10, self.width(), self.height() - 15
        coordsBody = [QPointF(w-r, 0), QPointF(w, r), QPointF(w, h-r),
                      QPointF(w-r, h), QPointF(r, h), QPointF(0, h-r), QPointF(0, r)]
        buttonShape = QPainterPath()
        buttonShape.moveTo(r, 0)
        for i in coordsBody:
            buttonShape.lineTo(i)

        buttonShape.closeSubpath()
        painter.drawPath(buttonShape)

        # Drawing the Design
        coordsOuterLine = [QPointF(w-2*r, r), QPointF(w-r, 2*r), QPointF(w-r, h-2*r),
                           QPointF(w-2*r, h-r), QPointF(2*r, h-r), QPointF(r, h-2*r), QPointF(r, 2*r)]
        coordsInnerLine = [QPointF(w-2*r-5, r+5), QPointF(w-r-5, 2*r+5), QPointF(w-r-5, h-2*r-5),
                           QPointF(w-2*r-5, h-r-5), QPointF(2*r+5, h-r-5), QPointF(r+5, h-2*r-5), QPointF(r+5, 2*r+5)]

        outerLinePath = QPainterPath()
        outerLinePath.moveTo(2*r, r)
        innerLinePath = QPainterPath()
        innerLinePath.moveTo(2*r+5, r+5)

        for j in coordsOuterLine:
            outerLinePath.lineTo(j)
        for k in coordsInnerLine:
            innerLinePath.lineTo(k)

        outerLinePath.closeSubpath()
        innerLinePath.closeSubpath()

        framePath = QPainterPath()
        framePath.setFillRule(Qt.FillRule.OddEvenFill)
        framePath.addPath(outerLinePath)
        framePath.addPath(innerLinePath)

        painter.setBrush(QBrush("#561B06", Qt.BrushStyle.Dense4Pattern))
        painter.drawPath(framePath)

        # Drawing the Text
        # Our font to write Text
        self.fontID1 = QFontDatabase.addApplicationFont(
            "./assets/fonts/Cinzel-Regular.otf")
        self.Cinzel = QFont(
            QFontDatabase.applicationFontFamilies(self.fontID1), 20)

        self.Cinzel.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
        painter.setFont(self.Cinzel)
        # painter.drawText(self.rect().adjusted(0, -3, 0, -3),
        #                  Qt.AlignmentFlag.AlignCenter, self.btnText)

        # Drawing and writing the button press logic
        innerShape = QPainterPath()
        innerShape.moveTo(0, h-r)
        innerShape.lineTo(r, h)
        innerShape.lineTo(w-r, h)
        innerShape.lineTo(w, h-r)
        innerShape.lineTo(w, h)
        innerShape.lineTo(w-r, h+10)
        innerShape.lineTo(r, h+10)
        innerShape.lineTo(0, h)
        innerShape.closeSubpath()

        painter.drawPath(innerShape)
        painter.setPen(QPen(QColor("#561B06"), 2))

        painter.drawLines([QPointF(0, h-r), QPointF(0, h), QPointF(0, h),
                           QPointF(r, h+10), QPointF(r, h + 10),
                           QPointF(w-r, h+10), QPointF(w-r, h+10),
                           QPointF(w, h), QPointF(w, h-r), QPointF(w, h)])
        painter.drawLine(r, h, r, h+10)
        painter.drawLine(w-r, h, w-r, h+10)


class outputPaper(QLabel):

    getEditorInTrashToo = Signal()
    getHimBack = Signal()
    getBlankPageAgain = Signal()

    disableButton = Signal()
    enableButton = Signal()

    PlayPrintSound = Signal()
    PlayBlankSound = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isNewPage = None
        self.isTrashPage = None
        self.paperMargin = 10
        self.readyForVanish = False

        self._offset = 0
        self._cutOffSet = 0
        self.paperOutDuration = 2200

        self.output = None

    def setNewPage(self, value, output=None):
        self.isNewPage = value
        self.output = output

    def setTrashPage(self, value):
        self.isTrashPage = value

    # Main Function
    def run(self, isSignalSender=False):
        if self.isNewPage:
            self.doBlankPageAnimation()
            if self.output == None:
                self.PlayBlankSound.emit()
            else:
                self.PlayPrintSound.emit()
        if self.isTrashPage:
            self.getToTrash()


# ANIMATION CODES

    def getToTrash(self):

        self.getEditorInTrashToo.emit()

        x, y, w, h = 20, 213, 220, 230
        self.moveAnim = QPropertyAnimation(self, b"geometry")
        self.moveAnim.setStartValue(QRect(x, y, w, h))
        self.moveAnim.setEndValue(QRect(x, y + h + 5, w, 0))
        self.moveAnim.setDuration(self.paperOutDuration)
        self.moveAnim.finished.connect(
            lambda: self.setGeometry(20, 213, 220, 0))
        self.moveAnim.finished.connect(lambda: self.vanisher(False))
        self.moveAnim.finished.connect(self.enableButton.emit)
        self.moveAnim.start()

    def doBlankPageAnimation(self):
        w, h = 220, 230
        self._cutOffSet = 0
        self.xAnim = QPropertyAnimation(self, b"size")
        self.xAnim.setStartValue(QSize(w, 0))
        self.xAnim.setEndValue(QSize(w, h))
        self.xAnim.setDuration(self.paperOutDuration)
        self.xAnim.finished.connect(self.detachAnimPhase)

        self.lineMovingAnim = QPropertyAnimation(self, b"offset")
        self.lineMovingAnim.setStartValue(-240)
        self.lineMovingAnim.setEndValue(0)
        self.lineMovingAnim.setDuration(self.paperOutDuration)

        self.runTogether = QParallelAnimationGroup(self)
        self.runTogether.addAnimation(self.xAnim)
        self.runTogether.addAnimation(self.lineMovingAnim)
        self.runTogether.start()

    def detachAnimPhase(self):
        # Clip animation
        self.cutAnim = QPropertyAnimation(self, b"cutOffSet")
        self.cutAnim.setStartValue(0)
        self.cutAnim.setEndValue(30)
        self.cutAnim.setDuration(self.paperOutDuration - 2000)
        self.cutAnim.finished.connect(lambda: self.vanisher(True))
        if self.output == None:
            self.cutAnim.finished.connect(self.getHimBack.emit)
        else:
            self.disableButton.emit()
            waitTimer = QTimer(self)
            waitTimer.setSingleShot(True)
            waitTimer.timeout.connect(self.decorateForBlank)
            self.cutAnim.finished.connect(lambda: waitTimer.start(500))

        self.cutAnim.start()

    # To get blank page after output page.
    def decorateForBlank(self):
        self.getBlankPageAgain.emit()

    # Property

    def getOffSet(self):
        return self._offset

    def setOffSet(self, value):
        self._offset = value
        self.update()

    offset = Property(float, getOffSet, setOffSet)

    def getCutOffSet(self):
        return self._cutOffSet

    def setCutOffSet(self, value):
        self._cutOffSet = value
        self.update()

    cutOffSet = Property(float, getCutOffSet, setCutOffSet)

    # To vanish the lines
    def vanisher(self, value):
        if self.output == None:
            self.readyForVanish = value
            self.update()
        else:
            self.readyForVanish = False

    def paintEvent(self, e):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setClipRect(0, self._cutOffSet, self.width(),
                            self.height() - self._cutOffSet)

        painter.setPen("#888888")
        painter.setBrush("#FFFFFF")

        w = self.width()
        h = self.height()
        r = 8  # curve radius

        # ---------- CREATE FULL PAPER SHAPE ----------
        thePaperPath = QPainterPath()

        thePaperPath.moveTo(0, 0)
        thePaperPath.arcTo(0, -15, 8, 30, 180, 90)
        thePaperPath.arcTo(0, 15, 8, 30, 90, -90)
        thePaperPath.lineTo(8, 230)
        thePaperPath.lineTo(212, 230)
        thePaperPath.lineTo(212, 30)
        thePaperPath.arcTo(212, 15, 8, 30, 180, -90)
        thePaperPath.arcTo(212, -15, 8, 30, 270, 90)
        thePaperPath.closeSubpath()

        painter.drawPath(thePaperPath)

        # Drawing the lines.
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        # ellipse equations
        def xoF1Left(y): return 4 - math.sqrt(16*(1 - (y**2/225)))
        def xoF2Left(y): return 4 + math.sqrt(16*(1 - ((y - 30)**2/225)))

        def xoF1Right(y): return 216 + math.sqrt(16*(1 - (y**2/225)))
        def xoF2Right(y): return 216 - math.sqrt(16*(1 - ((y - 30)**2/225)))

        penColor = "#888888"

        if self.output == None:
            penColor = "#888888"
        elif self.output == 'Spam':
            penColor = "#FF7878"
        elif self.output == 'Not Spam':
            penColor = "#78FF78"

        Brush = QBrush(penColor)
        Brush.setStyle(Qt.BrushStyle.DiagCrossPattern)

        painter.setPen(penColor)
        painter.save()

        if self.output == None:
            for i in range(15):
                y = self._offset + 20 * i  # 20 is line spacing in our editor
                if 0 <= y <= 15:
                    painter.drawLine(QPointF(xoF1Left(y) + self.paperMargin, y),
                                     QPointF(xoF1Right(y) - self.paperMargin, y))
                elif 15 < y <= 30:
                    painter.drawLine(QPointF(xoF2Left(y) + self.paperMargin, y),
                                     QPointF(xoF2Right(y) - self.paperMargin, y))
                else:
                    painter.drawLine(QPointF(8 + self.paperMargin, y),
                                     QPointF(212 - self.paperMargin, y))
        else:
            painter.setBrush(Brush)
            for i in range(15):
                y = self._offset + 20 * i  # 20 is line spacing in our editor
                if 0 <= y <= 15:
                    painter.drawRect(xoF1Left(y) + self.paperMargin, y,
                                     xoF1Right(y) - xoF1Left(y) - (self.paperMargin * 2), 8)
                elif 15 < y <= 30:
                    painter.drawRect(xoF2Left(y) + self.paperMargin, y,
                                     xoF2Right(y) - xoF2Left(y) - (self.paperMargin * 2), 8)
                else:
                    painter.drawRect(8 + self.paperMargin, y,
                                     204 - (self.paperMargin * 2), 8)

            # The STAMP
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            painter.setBrush(QBrush(penColor, Qt.BrushStyle.BDiagPattern))
            ellipsePen = QPen(QColor(penColor), 5)
            painter.setPen(ellipsePen)

            painter.drawEllipse(QPointF(110, self._offset + 130), 50, 50)

            ellipsePen.setWidth(2)
            painter.setPen(ellipsePen)
            painter.drawEllipse(QPointF(110, self._offset + 130), 45, 45)

            # Font to write spam or not spam
            fontID1 = QFontDatabase.addApplicationFont(
                "./assets/fonts/SpecialElite-Regular.ttf")
            specialElite = QFont(
                QFontDatabase.applicationFontFamilies(fontID1), 20)

            painter.setFont(specialElite)
            painter.drawText(QRect(60, self._offset + 80, 100, 100),
                             "Not\nSpam" if self.output == 'Not Spam' else "Spam", Qt.AlignmentFlag.AlignCenter)

        painter.restore()

        if self.readyForVanish:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush("#FFFFFF")
            painter.drawRect(9, self._cutOffSet, self.width() - 18,
                             self.height() - self._cutOffSet)


class NotebookTextEdit(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trashDuration = 1800

        # trigger repaint when scrolling
        self.verticalScrollBar().valueChanged.connect(self.viewport().update)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Our font for the editor
        self.fontID1 = QFontDatabase.addApplicationFont(
            "./assets/fonts/VictorMono-Regular.ttf")
        self.VictorMono = QFont(
            QFontDatabase.applicationFontFamilies(self.fontID1))
        self.VictorMono.setPixelSize(14)

        self.setFont(self.VictorMono)

    def getInTrash(self):
        x, y, w, h = self.x(), self.y(), self.width(), self.height()
        actualGeometry = self.geometry()
        self.trashAnim = QPropertyAnimation(self, b"geometry")
        self.trashAnim.setStartValue(QRect(x, y, w, h))
        self.trashAnim.setEndValue(QRect(x, y + h + 5, w, 0))
        self.trashAnim.setDuration(self.trashDuration)
        self.trashAnim.start()

    def paintEvent(self, event):

        painter = QPainter(self.viewport())
        painter.setPen("#888888")

        line_spacing = self.fontMetrics().lineSpacing()

        block = self.firstVisibleBlock()

        offset = self.blockBoundingGeometry(block).translated(
            self.contentOffset()
        ).top()

        height = self.viewport().height()
        width = self.viewport().width()

        y = offset

        # move grid to nearest spacing anchor
        while y > 0:
            y -= line_spacing

        while y < height:
            painter.drawLine(0, int(y), width, int(y))
            y += line_spacing

        super().paintEvent(event)


class body(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, e):
        r, w, h = 5, self.width(), self.height()

        painter = QPainter(self)

        # Drawing the background
        painter.setBrush("#E57F44")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, w, h-10, r, r)

        # Code for lines
        brownPen = QPen()
        brownPen.setColor("#AA705B")
        brownPen.setWidth(2)
        painter.setPen(brownPen)

        for i in range(1, 13):
            painter.drawLine(0, i * 26, self.width(), i * 26)

        # Code for nails
        stoneBrownPen = QPen()
        stoneBrownPen.setColor("#625B56")

        painter.setPen(stoneBrownPen)
        painter.setBrush("#625B56")

        for i in range(7, 310, 26):
            painter.drawEllipse(self.width() - 26, i, 11, 11)

        painter.setBrush("#561B06")
        painter.setPen(Qt.PenStyle.NoPen)

        underShape = QPainterPath()
        underShape.moveTo(0, h-3*r)
        underShape.lineTo(0, h-r)
        underShape.arcTo(0, h-2*r, 2*r, 2*r, 180, 90)
        underShape.lineTo(w-r, h)
        underShape.arcTo(w-2*r, h-2*r, 2*r, 2*r, 270, 90)
        underShape.lineTo(w, h-3*r)
        underShape.arcTo(w-2*r, h-4*r, 2*r, 2*r, 0, -90)
        underShape.lineTo(r, h-2*r)
        underShape.arcTo(0, h-4*r, 2*r, 2*r, 270, -90)

        underShape.closeSubpath()

        painter.drawPath(underShape)


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clickTime = 0
        self.output2Trash = True
        self.f1, self.t1, self.f2, self.t2 = False, True, True, False

        self.fontID = QFontDatabase.addApplicationFont(
            "./assets/fonts/Cinzel-Regular.otf")
        self.CinzelFont = QFont(
            QFontDatabase.applicationFontFamilies(self.fontID), 10)

        # The media
        self.bgPlayer = QMediaPlayer(self)
        self.bgAudio = QAudioOutput(self)

        self.bgPlayer.setAudioOutput(self.bgAudio)
        self.bgPlayer.setSource(
            QUrl.fromLocalFile("./assets/sounds/bg sound [Asher Fulero Ceremonial Library].mp3"))
        self.bgPlayer.setLoops(QMediaPlayer.Loops.Infinite)
        self.bgAudio.setVolume(0.7)

        self.printSound = QSoundEffect(self)
        self.printSound.setSource(
            QUrl.fromLocalFile("./assets/sounds/Printing.wav"))
        self.printSound.setVolume(0.7)

        self.blankSound = QSoundEffect(self)
        self.blankSound.setSource(QUrl.fromLocalFile(
            "./assets/sounds/freesound_community-printer-scan-68679.wav"))
        self.blankSound.setVolume(0.7)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(600, 490)

        self.background = body(self)
        self.background.setGeometry(0, 150, self.width(), self.height() - 150)

        self.titleBar = titleBar(self)
        self.titleBar.setGeometry(0, 80, 600, 145)

        self.newPaper = Paper(self)
        self.newPaper.setGeometry(20, 0, 220, 100)
        self.newPaper.disableButtonSignal.connect(
            lambda: self.checkBtn.setEnabled(False))
        self.newPaper.disableButtonSignal.connect(
            lambda: self.checkBtn.setIn(False))
        self.newPaper.enableButtonSignal.connect(
            lambda: self.actualTextEditor.show())
        self.newPaper.enableButtonSignal.connect(
            lambda: self.checkBtn.setIn(True))
        self.newPaper.enableButtonSignal.connect(
            lambda: self.checkBtn.setBtnText("CHECK"))

        self.checkBtn = checkBtn("START", self)
        self.checkBtn.setGeometry(320, 352, 230, 75)
        self.checkBtn.clicked.connect(lambda: self.newPaper.comeOut())
        self.checkBtn.clicked.connect(
            lambda: self.startMachine(self.f1, self.t1, self.f2, self.t2, False))
        if self.clickTime == 0:
            self.checkBtn.clicked.connect(self.bgPlayer.play)

        self.settingsLabel = settingsPanel(self)
        self.settingsLabel.setGeometry(320, 180, 230, 150)

        self.bgMusicLabel = QLabel("bg music", self)
        self.bgMusicLabel.setFont(self.CinzelFont)
        self.bgMusicLabel.setGeometry(
            350, self.settingsLabel.y() + 20, 100, 20)
        self.bgMusicLabel.setStyleSheet(
            "QLabel{color: #561B06;}")

        self.bgMusicSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.bgMusicSlider.setGeometry(
            350, self.bgMusicLabel.y() + 15, 170, 30)
        self.bgMusicSlider.setStyleSheet('''
                            QSlider::groove:horizontal {
                                height: 3px;
                                background: transparent;
                                border: 2px solid #DD7E5C;
                                border-radius: 3px;
                            }

                            QSlider::handle:horizontal {
                                background: #CA633E;
                                width: 15px;
                                height: 15px;
                                border-radius: 5px;
                                border: 3px solid #793B25;
                                margin: -4px 0;
                            }
                            QSlider::sub-page:horizontal {
                                background: #561B06;
                                border: 2px solid #DD7E5C;
                                border-radius: 3px;}''')
        self.bgMusicSlider.setRange(0, 100)
        self.bgMusicSlider.setValue(70)
        self.bgMusicSlider.valueChanged.connect(
            lambda: self.bgAudio.setVolume(self.bgMusicSlider.value() / 100))

        self.printerMusicLabel = QLabel("printer sound", self)
        self.printerMusicLabel.setFont(self.CinzelFont)
        self.printerMusicLabel.setGeometry(
            350, self.bgMusicSlider.y() + 40, 120, 20)
        self.printerMusicLabel.setStyleSheet(self.bgMusicLabel.styleSheet())

        self.printerMusicSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.printerMusicSlider.setGeometry(
            350, self.printerMusicLabel.y() + 15, 170, 30)
        self.printerMusicSlider.setStyleSheet(self.bgMusicSlider.styleSheet())
        self.printerMusicSlider.setRange(0, 100)
        self.printerMusicSlider.setValue(70)
        self.printerMusicSlider.valueChanged.connect(
            lambda: self.printSound.setVolume(self.printerMusicSlider.value() / 100))
        self.printerMusicSlider.valueChanged.connect(
            lambda: self.blankSound.setVolume(self.printerMusicSlider.value() / 100))

        self.outputPaper1 = outputPaper(self)
        self.outputPaper1.setGeometry(20, 213, 220, 0)

        self.outputPaper2 = outputPaper(self)
        self.outputPaper2.setGeometry(20, 213, 220, 0)

        # The Text Editor Code
        self.actualTextEditor = NotebookTextEdit(self)
        self.actualTextEditor.setGeometry(36, 248, 189, 190)
        self.actualTextEditor.setStyleSheet(
            '''QPlainTextEdit{
            background: transparent; color: black;}''')
        self.actualTextEditor.hide()

        # To get editor in trash too
        papers = [self.outputPaper1, self.outputPaper2]

        for paper in papers:
            paper.getEditorInTrashToo.connect(
                self.actualTextEditor.getInTrash)
            paper.getHimBack.connect(self.resetEditor)
            paper.getBlankPageAgain.connect(
                lambda: self.startMachine(self.f1, self.t1, self.f2, self.t2, True))
            paper.getBlankPageAgain.connect(self.newPaper.comeOut)
            paper.PlayPrintSound.connect(lambda: self.printSound.play())
            paper.PlayBlankSound.connect(lambda: self.blankSound.play())

        self.closeBtn = QPushButton("Close", self)
        self.closeBtn.setFont(self.actualTextEditor.VictorMono)
        self.closeBtn.setGeometry(520, 85, 70, 25)
        self.closeBtn.setStyleSheet('''QPushButton{
                                        color: #95BCCB;
                                        font-weight: bold;
                                        background-color: #E5F5FA;
                                        border: 2px solid #95BCCB;
                                        border-radius: 5px}''')
        self.closeBtn.clicked.connect(self.close)

        self.aboutBtn = QPushButton("i", self)
        self.aboutBtn.setFont(self.actualTextEditor.VictorMono)
        self.aboutBtn.setGeometry(480, 85, 25, 25)
        self.aboutBtn.setStyleSheet('''QPushButton{
                                        color: #95BCCB;
                                        font-weight: 900;
                                        background-color: #046D97;
                                        border-radius: 12px;}''')
        self.aboutBtn.clicked.connect(self.openAbout)

    def resetEditor(self):
        self.actualTextEditor.clear()
        self.actualTextEditor.setGeometry(36, 248, 189, 190)
        self.actualTextEditor.setFocus()
        self.checkBtn.setEnabled(True)

    def startMachine(self, f1, t1, f2, t2, isBlank):
        output = None
        if self.clickTime > 0:
            if isBlank:
                output = None
            else:
                output = checkStatus(self.actualTextEditor.toPlainText())

            if self.output2Trash:
                self.outputPaper1.setNewPage(not f1, output)
                self.outputPaper1.setTrashPage(not t1)
                self.outputPaper2.setNewPage(not f2, checkStatus(
                    self.actualTextEditor.toPlainText()))
                self.outputPaper2.setTrashPage(not t2)
            else:
                self.outputPaper1.setNewPage(not f1, checkStatus(
                    self.actualTextEditor.toPlainText()))
                self.outputPaper1.setTrashPage(not t1)
                self.outputPaper2.setNewPage(not f2, output)
                self.outputPaper2.setTrashPage(not t2)

            self.outputPaper1.run()
            self.outputPaper2.run()

            self.output2Trash = not self.output2Trash
            self.f1, self.t1, self.f2, self.t2 = not f1, not t1, not f2, not t2

        else:
            self.outputPaper1.setNewPage(False)
            self.outputPaper1.setTrashPage(False)
            self.outputPaper2.setNewPage(True)
            self.outputPaper2.setTrashPage(False)

            self.outputPaper1.run()
            self.outputPaper2.run()

            self.clickTime = 1

    def openAbout(self):
        aboutDialog = AboutDialog()
        aboutDialog.exec()


app = QApplication(sys.argv)
window = mainWindow()
window.show()

sys.exit(app.exec())
