import cv2
import numpy as np
import autocar_module as m

capture = cv2.VideoCapture('road.mp4')
count = 0
if capture.isOpened():
    while True:
        sucess, img = capture.read()
        if sucess:
            # img = cv2.imread('road.jpg')
            edge = m.get_edge(img)
            roi = m.get_roi(edge)

            lines = cv2.HoughLinesP(image=roi,
                                    rho=3,
                                    theta=np.pi / 180,
                                    threshold=50,
                                    minLineLength=60,
                                    maxLineGap=300)
            # print(lines.shape)
            avglines = m.get_avglines(lines)

            if avglines is not None:
                lines = m.get_sublines(img, avglines)
                # print(lines)
                img = m.draw_lines(img, lines)
            else:
                print('Can not find lines')

            # cv2.imshow('Edge', edge)
            # cv2.imwrite('Edge.jpg', edge)
            # cv2.imshow('Roi', roi)
            # cv2.imwrite('Roi.jpg', roi)
            cv2.imshow('Line', img)
            cv2.imwrite(str(count)+'.jpg', img)
            count += 1
        k = cv2.waitKey(100)
        if k == ord('q') or k == ord('Q'):
            print('exit')
            cv2.destroyAllWindows()
            capture.release()
            break
