from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About Spam Detector")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout(self)

        title = QLabel("<h2>Spam Detector</h2>")
        title.setAlignment(Qt.AlignLeft)

        info = QLabel(
            "Version: 1.0\n"
            "Developer: Jatin Verma\n"
            "Built with: PySide6\n\n"
            "First Release 🚀\n"
            "Assets Credits:\n"
            "- SOUNDS:\n"
            "  > Printing.wav -- deadsounds.com\n"
            "  > freesound_community-printer-scan-68679.wav -- freesound \ncommunity from #Pixaboy\n"
            "  > bg sound -- Ceremonial Library (by Asher Fulero)\n\n"
            "- FONTS:\n"
            "  > Victor Mono by Rune Bjørnerås (rubjo.github.io/victor-mono)\n"
            "  > Cinzel by Natanael Gama (Google Fonts)\n"
            "  > SpecialElite by Astigmatic (Google Fonts)\n"
            "  > BeautifulES by Ellen Luff\n"
        )

        copy_btn = QPushButton("Copy")
        ok_btn = QPushButton("OK")

        copy_btn.clicked.connect(
            lambda: QApplication.clipboard().setText(info.text())
        )
        ok_btn.clicked.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(copy_btn)
        layout.addWidget(ok_btn)
