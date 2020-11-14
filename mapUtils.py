import cv2


def readMap(mapFileName):
    mapFile = open(mapFileName, "r")
    lines = mapFile.readlines()
    map = []
    for line in lines:
        line =line.split(',')
        line = [int(x) for x in line]
        map.append(line)
    return map

def writeMap(imageFileName, mapFileName):
    mapFile = open(mapFileName, "w")
    img = cv2.imread(imageFileName, 0)
    height, width = img.shape
    for i in range(height):
        for j in range(width):
            if img[i][j] > 127:
                mapFile.write('1')
            else:
                mapFile.write('0')
            if j != width - 1:
                mapFile.write(',')
        if i != height - 1:
            mapFile.write('\n')
    mapFile.close()
    print("Map saved to file: ", mapFileName)
    cv2.imshow(imageFileName, img)
    cv2.waitKey(0)


if __name__ == "__main__":
    writeMap("map.png", "map.txt")
