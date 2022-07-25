import os
from wand.image import Image
from natsort import os_sorted
import math

# CONFIG

sourceFolder = "input/"
destinationFolder = "output/"
maxSize = 3000
rightToLeft = False

# END CONFIG


def getListFiles(sourceFolder):
    files = os_sorted(os.listdir(sourceFolder))
    #files = [file for file in files if not file.startswith("_")]
    return files


def resizeAndSave(image, savePath):
    height = image.height

    newHeight = min(maxSize, height)
    newWidth = newHeight * meanRatio

    image.transform(resize=str(newWidth) + "x" + str(newHeight) + "!")

    image.compression_quality = 75
    image.save(filename=savePath)


def savePath():
    return destinationFolder + str(saveIndex) + ".webp"


# Read all the widths and heights from the images

widths = []
heights = []
ratios = []
for file in getListFiles(sourceFolder):
    path = sourceFolder + file + '[0]'
    image = Image(filename=path)
    widths += [image.width]
    heights += [image.height]
    ratios += [image.width / image.height]
    print(file, image.orientation, ratios[-1])

ratios.sort()

if (ratios[-1] > ratios[0] * 1.5):
    medianRatio = (ratios[-1] + ratios[0]) / 2
    groupA = [e for e in ratios if e < medianRatio]
    groupB = [e for e in ratios if e >= medianRatio]

    meanRatioA = sum(groupA) / len(groupA)
    meanRatioB = sum(groupB) / 2 / len(groupB)

    meanRatio = (meanRatioA + meanRatioB) / 2

    print(meanRatioA, meanRatioB, meanRatio)

else:
    meanRatio = sum(ratios) / len(ratios)
    print(meanRatio)


# Convert and split the images

saveIndex = 1
for file in getListFiles(sourceFolder):
    path = sourceFolder + file + '[0]'
    image = Image(filename=path)

    height = image.height
    width = image.width

    if (width > height):

        # Double page
        left = image.clone()
        left.crop(0, 0, math.floor(width / 2), height)

        right = image.clone()
        right.crop(math.ceil(width / 2), 0, width, height)

        if (rightToLeft):
            resizeAndSave(right, savePath())
            saveIndex += 1
            resizeAndSave(left, savePath())
            saveIndex += 1
        else:
            resizeAndSave(left, savePath())
            saveIndex += 1
            resizeAndSave(right, savePath())
            saveIndex += 1

    else:
        resizeAndSave(image, savePath())
        saveIndex += 1

    print(file, "DONE")
