# sif-icon-generator
An [LLSIF-style icon generator](https://www.kongzhu.me/tech/icon-generator.html) implementation. Use PNG anime image files to generate LLSIF-style UR card icon.
## Dependencies
* numpy
* opencv
* [animeface](https://github.com/nya3jp/python-animeface)
## Usage
* Single file: `python utils.py --file ./example.png --smile --pure --cool --savepath ./result.png`
* Directory: `python utils.py --dir ./img/ --smile --pure --cool --savepath ./result/`
