import cv2
import numpy as np


def get_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (13, 13), 0)  # img, kernel_size, std
    canny = cv2.Canny(blur, 50, 150)  # img, low_threshold, high_threshold
    return canny


def get_roi(img):
    mask = np.zeros_like(img)
    points = np.array([[[146, 536],
                        [781, 539],
                        [515, 417],
                        [296, 397]]])
    cv2.fillPoly(mask, points, 255)
    roi = cv2.bitwise_and(img, mask)
    return roi


def draw_lines(img, lines):
    for line in lines:
        points = line.reshape(4, )  # (1, 4) to (4, )
        x1, y1, x2, y2 = points
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # image, start_coordinate, end_coordinate, color, line_width
    return img


def get_avglines(lines):
    if lines is None:
        print('Can not find lines')
        return None

    lefts, rights = ([] for _ in range(2))
    for line in lines:
        points = line.reshape(4, )
        x1, y1, x2, y2 = points
        slope, bias = np.polyfit((x1, x2), (y1, y2), 1)
        # y= slope*x +b
        # print(f'y = {slope} x + {bias}')
        if slope > 0:
            rights.append([slope, bias])
        else:
            lefts.append([slope, bias])

    if rights and lefts:  # rights and lefts are not None
        right_avg = np.average(rights, axis=0)
        left_avg = np.average(lefts, axis=0)
        return np.array([right_avg, left_avg])
    else:
        print('can not find rights and lefts')
        return None


def get_sublines(img, avglines):
    sublines = []
    for line in avglines:
        slope, bias = line
        y1 = img.shape[0]
        y2 = int(y1 * (3 / 5))
        x1 = (int(y1 - bias) / slope)
        x2 = (int(y2 - bias) / slope)
        sublines.append([x1, y1, x2, y2])
    return np.array(sublines, dtype=int)
