import cv2
import numpy as np


def image_process(src):
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = dst[90:390, 170:470]
    edged = cv2.Canny(dst, 100, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    contours_mat, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = np.array(contours_mat)
    xvalue, yvalue = [], []
    x_min, x_max, y_min, y_max = 0, 7, 0, 7
    for i in contours:
        for j in i:
            xvalue.append(j[0][0])
            yvalue.append(j[0][1])
            x_min = min(xvalue)
            x_max = max(xvalue)
            y_min = min(yvalue)
            y_max = max(yvalue)

    img_trim = dst[y_min:y_max, x_min:x_max]
    try:
        img_trim = cv2.resize(img_trim, dsize=(300, 300), interpolation=cv2.INTER_LINEAR_EXACT)
        _, fin = cv2.threshold(img_trim, 90, 255, cv2.THRESH_BINARY)
        return cmp(fin)
    except:
        return 1


def cmp(src):
    a = ['A', 'B', 'C', 'D', 'E', 'W', 'N', 'S', 'Left_Arrow', 'Right_Arrow']
    c = 1000000
    alphabet = ''
    for i in a:
        cnt = 0
        ori = cv2.imread("./samples/sample_{0}.png".format(i), cv2.IMREAD_GRAYSCALE)
        cmp = ori ^ src
        for j in cmp:
            for k in j:
                if int(k) == 255:
                    cnt += 1
        if c > cnt:
            alphabet = i
            c = cnt
    if c >= 30000:
        return 0
    return alphabet


i = 0

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:
    i += 1
    ret, frame = capture.read()
    if i % 30 == 0:
        print(image_process(frame))
    cv2.rectangle(frame, (168, 88, 300, 300), (255, 0, 0), 1)
    cv2.imshow("VideoFrame", frame)

capture.release()
cv2.destroyAllWindows()
