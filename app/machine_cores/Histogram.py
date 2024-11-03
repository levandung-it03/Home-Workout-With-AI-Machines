import cv2, os
import matplotlib.pyplot as plt

img = cv2.imread(os.path.join(os.getcwd(), "app/dataset/img/body_fat_detection/male/8_4.png"))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
regular_eq_hist = cv2.equalizeHist(gray_img)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
clahe_eq_hist = clahe.apply(gray_img)

plt.figure(figsize=(15, 15))
plt.subplot(3,2,1), plt.imshow(gray_img, cmap='gray'), plt.title("Input"), plt.axis("off")
plt.subplot(3,2,2), plt.hist(gray_img.ravel(), bins=256), plt.title("Input Histogram")
plt.subplot(3,2,3), plt.imshow(regular_eq_hist, cmap='gray'), plt.title("Output Regular"), plt.axis("off")
plt.subplot(3,2,4), plt.hist(regular_eq_hist.ravel(), bins=256), plt.title("Output Regular")
plt.subplot(3,2,5), plt.imshow(clahe_eq_hist, cmap='gray'), plt.title("Output CLAHE"), plt.axis("off")
plt.subplot(3,2,6), plt.hist(clahe_eq_hist.ravel(), bins=256), plt.title("Output CLAHE")
plt.show()
