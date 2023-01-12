# Модуль для работы с директорией
import os
# Модуль для обработки картиночек
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)

app = QApplication([])
win = QWidget()

btn_dir = QPushButton('Папка')
btn_list = QListWidget()
picture = QLabel('')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/б')

win.resize(700, 400)
win.setWindowTitle('Not So Easy Editor')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(btn_list)
col2.addWidget(picture)
row_of_tools = QHBoxLayout()
row_of_tools.addWidget(btn_left)
row_of_tools.addWidget(btn_right)
row_of_tools.addWidget(btn_mirror)
row_of_tools.addWidget(btn_sharp)
row_of_tools.addWidget(btn_bw)
col2.addLayout(row_of_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

workdir = ''


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenameslist():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    btn_list.clear()
    for filename in filenames:
        btn_list.addItem(filename)


btn_dir.clicked.connect(showFilenameslist)


class ImageProcessor():
    def __init__(self, image=None, filename=None, save_dir=''):
        self.image = image
        self.filename = filename
        self.save_dir = save_dir

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)


workimage = ImageProcessor()


def showChosenImage():
    if btn_list.currentRow() >= 0:
        filename = btn_list.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


btn_list.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.rotate_left)
btn_right.clicked.connect(workimage.rotate_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharp)

win.show()
app.exec()