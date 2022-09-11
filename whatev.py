import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.morphology import binary_erosion, reconstruction
from skimage.morphology.convex_hull import convex_hull_image


# https://stackoverflow.com/a/54481969/11089932
def simple_white_balancing(image):
    h, w = image.shape[:2]
    patch = image[int(h / 2 - 20):int(h / 2 + 20), int(w / 2 - 20):int(w / 2 + 20)]
    x, y = cv2.minMaxLoc(np.sum(patch.astype(int), axis=2))[3]
    white_b, white_g, white_r = patch[y, x, ...].astype(float)
    lum = (white_r + white_g + white_b) / 3
    image[..., 0] = image[..., 0] * lum / white_b
    image[..., 1] = image[..., 1] * lum / white_g
    image[..., 2] = image[..., 2] * lum / white_r
    return image


for file in ['mazes/maze.png']:
    # Read image
    img = cv2.imread(file)

    # Initialize hull image
    h, w = img.shape[:2]
    hull = np.zeros((h, w), np.uint8)

    # Simple white balancing, cf. https://stackoverflow.com/a/54481969/11089932
    img = cv2.GaussianBlur(img, (11, 11), None)
    maze = simple_white_balancing(img.copy())

    # Mask low saturation area
    sat = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)[..., 1]
    mask = (sat < 16).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_RECT,
                                                      (31, 31)))
    mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                            cv2.getStructuringElement(cv2.MORPH_RECT,
                                                      (201, 201)))

    # Find largest contour in mask (w.r.t. the OpenCV version)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnt = max(cnts, key=cv2.contourArea)
    cnt = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)

    # Crop to low saturation area
    cut = cv2.cvtColor(maze[y + 1:y + 1 + h, x + 1:x + 1 + w], cv2.COLOR_BGR2GRAY)

    # Use existing reconstruction approach on low saturation area
    h_c, w_c = cut.shape
    seed = np.zeros_like(cut)
    size = 40
    hh = h_c // 2
    hw = w_c // 2
    seed[hh - size:hh + size, hw - size:hw + size] = cut[hh - size:hh + size, hw - size:hw + size]
    rec = reconstruction(seed, cut)
    rec = cv2.erode(rec, np.ones((2, 2)), iterations=1)

    seed = np.ones_like(rec) * 255
    size = 240
    seed[hh - size:hh + size, hw - size:hw + size] = rec[hh - size:hh + size, hw - size:hw + size]
    rec = reconstruction(seed, rec, method='erosion').astype(np.uint8)
    rec = cv2.threshold(rec, np.quantile(rec, 0.25), 255, cv2.THRESH_BINARY_INV)[1]

    hull[y + 1:y + 1 + h, x + 1:x + 1 + w] = convex_hull_image(rec) * 255

    plt.figure(figsize=(18, 8))
    plt.subplot(1, 5, 1), plt.imshow(img[..., ::-1]), plt.title('Original image')
    plt.subplot(1, 5, 2), plt.imshow(maze[..., ::-1]), plt.title('White balanced image')
    plt.subplot(1, 5, 3), plt.imshow(sat, 'gray'), plt.title('Saturation channel')
    plt.subplot(1, 5, 4), plt.imshow(hull, 'gray'), plt.title('Obtained convex hull')
    plt.subplot(1, 5, 5), plt.imshow(cv2.bitwise_and(img, img, mask=hull)[..., ::-1])
    plt.tight_layout(), plt.savefig(file + 'output.png'), plt.show()
