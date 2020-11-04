# import libraries
import cv2
import numpy as np

# callback mouse event
def blemishRemovalFcn(action, x, y, flags, userdata):
    global image, img
    if action == cv2.EVENT_LBUTTONDOWN:
        radius = 15
        roi = img[y-radius:y+radius, x-radius:x+radius, :].copy()
        bilateralImg = cv2.bilateralFilter(roi, d=20, sigmaColor=50, sigmaSpace=50)
        # clone seamlessly
        src = bilateralImg
        dst = img
        src_mask = 255*np.ones_like(src)
        center = (x,y)
        img = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)
        image = img.copy()
        # display image
        cv2.imshow(windowName, image)


# read image
image = cv2.imread("blemish.png", cv2.IMREAD_COLOR)

# copy image
img = image.copy()
dummy = image.copy()

# create window
windowName = "Blemish removal"
cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)

cv2.setMouseCallback(windowName, blemishRemovalFcn)

k = 0
while k != 27:
    cv2.imshow(windowName, image)
    cv2.putText(image, "Click to remove blemish.", (10, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.putText(image, "ESC: exit, s: save, r: restart", (10, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('s'):
        cv2.imwrite("newImage.png", img)
    if k == ord('r'):
        image = dummy.copy()
        img = dummy.copy()

cv2.destroyAllWindows()