import os
import pillow_heif
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HEIC to JPG Converter")
        self.setMinimumWidth(400)
        self.setMinimumHeight(250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()

        self.layout_1 = QVBoxLayout()

        self.label = QLabel("Выберите папку с фотографиями")
        self.layout_1.addWidget(self.label)

        self.load_folder_button_1 = QPushButton("Выбрать папку")
        self.load_folder_button_1.clicked.connect(self.select_load_folder)
        self.layout_1.addWidget(self.load_folder_button_1)

        self.load_folder_label = QLabel("")
        self.layout_1.addWidget(self.load_folder_label)

        self.main_layout.addLayout(self.layout_1)

        self.layout_2 = QVBoxLayout()

        self.label = QLabel("Выберите папку куда сохранить фотографии")
        self.layout_2.addWidget(self.label)

        self.button_2 = QPushButton("Выбрать папку")
        self.button_2.clicked.connect(self.select_save_folder)
        self.layout_2.addWidget(self.button_2)

        self.save_folder_label = QLabel("")
        self.layout_2.addWidget(self.save_folder_label)

        self.main_layout.addLayout(self.layout_2)

        self.button_3 = QPushButton("Конвертировать")
        self.button_3.clicked.connect(self.convert_images)
        self.main_layout.addWidget(self.button_3)

        self.central_widget.setLayout(self.main_layout)

        self.load_folder = None
        self.save_folder = None

    def select_load_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку", options=options)
        if folder:
            self.load_folder = folder
            self.load_folder_label.setText(folder)

    def select_save_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку", options=options)
        if folder:
            self.save_folder = folder
            self.save_folder_label.setText(folder)

    def convert_images(self):
        for file_name in os.listdir(self.load_folder):
            if file_name.endswith(".heic"):
                heic_file = os.path.join(self.load_folder, file_name)
                jpg_file = os.path.join(self.save_folder, f"{os.path.splitext(file_name)[0]}.jpeg")
                heif_file = pillow_heif.read_heif(heic_file)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                )
                image.save(jpg_file, format="jpeg")
                print(f"Файл {heic_file} успешно сконвертирован в {jpg_file}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
