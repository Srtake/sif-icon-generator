import img_deal
import argparse
import glob as gb
import os

parser = argparse.ArgumentParser()
parser.add_argument('--file', default='./example.png', help='path of source image')
parser.add_argument('--dir', default='', help = 'path of source image directory')
parser.add_argument('--smile', action='store_true', help='generate smile border icon')
parser.add_argument('--pure', action='store_true', help='generate pure border icon')
parser.add_argument('--cool', action='store_true', help='generate cool border icon')
parser.add_argument('--savepath', default='./result.png', help='path to save result image(s)')

opt = parser.parse_args()

if __name__ == "__main__":
    generator = img_deal.SIFIconGenerator()

    attrs = []
    if opt.smile:
        attrs.append(generator.smile)
    if opt.pure:
        attrs.append(generator.pure)
    if opt.cool:
        attrs.append(generator.cool)

    if opt.dir:
        sources = gb.glob(opt.dir + '*')
        for i in range(len(sources)):
            generator.utils(sources[i], attrs, opt.savepath + os.path.basename(sources[i]))
    
    else:
        generator.utils(opt.file, attrs, opt.savepath)


