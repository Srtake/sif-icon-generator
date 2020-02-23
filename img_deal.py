# coding:utf8

import face_detect
import numpy as np
import cv2

class SIFIconGenerator():
    def __init__(self):
        self.icon_border = ['./border/smile_border.png',
                            './border/pure_border.png', './border/cool_border.png']
        self.internal_size = 109
        self.internal_radius = (int)(self.internal_size / 2)
        self.external_size = 128
        self.external_radius = (int)(self.external_size / 2)
        self.padding = 10
        self.rgb_black = [0, 0, 0]
        self.attrs = ['smile', 'pure', 'cool']
        self.smile = 0
        self.pure = 1
        self.cool = 2

    def load(self, input_img):
        # Load -> pad -> get image shape
        self.img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
        self.img = cv2.copyMakeBorder(self.img, self.padding, self.padding, self.padding,
                                      self.padding, cv2.BORDER_CONSTANT, value=self.rgb_black)
        self.rows, self.cols, self.channel = self.img.shape

    def iconCircleMerge(self, x, y, delta_x, delta_y):
        #
        # Crop the image to a circle, and resize it to a fixed size (128x128)
        #

        # Result image (4 channels, initialized to a transparent image)
        rows, cols, channel = self.rows, self.cols, self.channel
        img_new = np.zeros((rows, cols, 4), np.uint8)
        img_new[:, :, 0:3] = self.img[:, :, 0:3]

        # Circle used to crop the source image
        # Initialized to the size of source image (will be resized later)
        # 1 channel (only alpha information needed)
        img_circle = np.zeros((rows, cols, 1), np.uint8)
        img_circle[:, :, :] = 0
        img_circle = cv2.circle(img_circle, ((int)(x + delta_x / 2), (int)(y + delta_y / 2)),
                                (int)(min(delta_x, delta_y) / 2), (255), -1)

        # Merge the circle and source image
        # Set alpha value of pixels in circle area to 255
        # and resize the image to a fixed size (128x128)
        img_new[:, :, 3] = img_circle[:, :, 0]
        img_new = cv2.resize(
            img_new[x:x+delta_x, y:y+delta_y, 0:4], (self.external_size, self.external_size))
        self.img = img_new

    def loadIconBorder(self, attr):
        return cv2.imread(self.icon_border[attr], cv2.IMREAD_UNCHANGED)

    def addSmileIconBorder(self):
        #
        # Add smile icon border to the image processed by iconCircleMerge()
        #

        # Load smile icon border image
        # and initialize result image (a copy of smile icon border image)
        border_smile = self.loadIconBorder(self.smile)
        border_new_smile = np.zeros(
            (self.external_size, self.external_size, 4), np.uint8)
        border_new_smile[:, :, 0:3] = border_smile[:, :, 0:3]
        border_new_smile[:, :, 3] = 255

        # Add pixels of source image to the internal circle
        for i in range(self.external_size):
            for j in range(self.external_size):
                if border_new_smile[i, j, 1] > border_new_smile[i, j, 0] and border_new_smile[i, j, 1] > border_new_smile[i, j, 2] and border_new_smile[i, j, 1] != 209:
                    border_new_smile[i, j, 0:3] = [255, 255, 255]
                if border_new_smile[i, j, 1] == 209:
                    border_new_smile[i, j, 0:3] = self.img[i, j, 0:3]
        return border_new_smile

    def addPureIconBorder(self):
        border_pure = self.loadIconBorder(self.pure)
        border_new_pure = np.zeros((self.external_size, self.external_size, 4), np.uint8)
        border_new_pure[:, :, 0:3] = border_pure[:, :, 0:3]
        border_new_pure[:, :, 3] = 255
        for i in range(self.external_size):
            for j in range(self.external_size):
                if border_new_pure[i, j, 2] > border_new_pure[i, j, 1] and border_new_pure[i, j, 2] > border_new_pure[i, j, 0] and border_new_pure[i, j, 2] != 236:
                    border_new_pure[i, j, 0:3] = [255, 255, 255]
                if border_new_pure[i, j, 2] == 236:
                    border_new_pure[i, j, 0:3] = self.img[i, j, 0:3]
        return border_new_pure

    def addCoolIconBorder(self):
        border_cool = self.loadIconBorder(self.cool)
        border_new_cool = np.zeros((self.external_size, self.external_size, 4), np.uint8)
        border_new_cool[:, :, 0:3] = border_cool[:, :, 0:3]
        border_new_cool[:, :, 3] = 255
        for i in range(self.external_size):
            for j in range(self.external_size):
                if border_new_cool[i, j, 2] > border_new_cool[i, j, 1] and border_new_cool[i, j, 2] > border_new_cool[i, j, 0] and border_new_cool[i, j, 2] != 236:
                    border_new_cool[i, j, 0:3] = [255, 255, 255]
                if border_new_cool[i, j, 2] == 236:
                    border_new_cool[i, j, 0:3] = self.img[i, j, 0:3]
        return border_new_cool

    def addIconBorder(self, attr):
        add_func = [self.addSmileIconBorder,
                    self.addPureIconBorder, self.addCoolIconBorder]
        return add_func[attr]()

    def save(self, img, path):
        cv2.imwrite(path, img)

    def utils(self, src, attr, path):
        #
        # utility of the class
        # src  - path of source image
        # attr - list of icon borders (smile/pure/cool)
        # path - path to save result image
        #

        # Load the image
        self.load(src)

        # Use animeface to detect face(s) in source image
        fd = face_detect.FaceDetector(path)
        face_pos = fd.detect()

        # Generate icon(s) using face position information
        for i in range(len(face_pos)):
            self.iconCircleMerge(face_pos[i].y, face_pos[i].x,
                                 face_pos[i].height, face_pos[i].width)
            for j in range(len(attr)):
                result = self.addIconBorder(attr[j])
                result_path = path.replace('.png', '-' + str(i) + '-' + str(self.attrs[attr[j]]) + '.png')
                self.save(result, result_path)
