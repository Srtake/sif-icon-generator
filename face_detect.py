from PIL import Image
import animeface
import os

class FaceDetector():
    def __init__(self, path):
        #
        # Save original image paths into a list
        #
        self.orig_path = path
    def detect(self):
        #
        # Detect faces in a given image using animeface API
        #
        im = Image.open(self.orig_path)
        faces = animeface.detect(im)
        faces_pos = []
        for i in range(len(faces)):
            faces_pos.append(faces[i].face.pos)
        for i in range(len(faces_pos)):
            long = min((int)(faces_pos[i].width * 3), (int)(faces_pos[i].height * 2.25))
            expand_pixels_width = (int)((long - faces_pos[i].width) / 2)
            expand_pixels_height = (int)((long - faces_pos[i].height) / 2)
            expanded_x = max(faces_pos[i].x - expand_pixels_width, 0)
            expanded_y = max(faces_pos[i].y - expand_pixels_height, 0)
            faces_pos[i].x = expanded_x
            faces_pos[i].y = expanded_y
            faces_pos[i].width = long
            faces_pos[i].height = long
        print('Detect ' + str(len(faces)) + ' faces.')
        return faces_pos
