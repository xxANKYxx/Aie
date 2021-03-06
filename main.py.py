# -*- coding: utf-8 -*-


#imported necessary functions
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as T
import torch
from torchvision import models
from PIL import Image
import sys
from skimage import io
import cv2

path='' #path of image to be manipulated
backpath='' #path of background image for background change

#image Decode Function converts 2D image into RGB image
# in coments the object ,atched have been mentioned with coressponding objets
import numpy as np
def decode_segmap(image, nc=21):
  label_colors = np.array([(0, 0, 0),  # 0=background
  # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
  (128, 0, 0), (0, 128, 0), (255, 255, 255), (0, 0, 128), (128, 0, 128),
  # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
  (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
  # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
  (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (255, 255, 255),
  # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
  (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])
  r = np.zeros_like(image).astype(np.uint8)
  g = np.zeros_like(image).astype(np.uint8)
  b = np.zeros_like(image).astype(np.uint8)
  for l in range(0, nc):
    idx = image == l
    r[idx] = label_colors[l, 0]
    g[idx] = label_colors[l, 1]
    b[idx] = label_colors[l, 2]
  rgb = np.stack([r, g, b], axis=2)
  return rgb

#  pre processing image(converting into tensor, Normalizing it)
import matplotlib.pyplot as plt
import torchvision.transforms as T
import torch
from PIL import Image
def segment(net, path, show_orig=True):
  img = Image.open(path)
  if show_orig: 
    plt.imshow(img); 
    plt.axis('off'); 
    plt.show()

  trf = T.Compose([T.ToTensor(),
  T.Normalize(mean = [0.485, 0.456, 0.406],
  std = [0.229, 0.224, 0.225])])
  inp = trf(img).unsqueeze(0)
  out = net(inp)['out']
  om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
  rgb = decode_segmap(om)
  return rgb

from torchvision import models
import PIL
dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()
rgb=segment(dlab,path)
## If there are multiple labeled objects in the image, use the below code to have only the target as the foreground
rgb[rgb!=255]=0

mask_out=cv2.subtract(rgb,img)
mask_out=cv2.subtract(rgb,mask_out)
mask_out[rgb == 0] = 255
# Display the result
#numpy_horizontal = np.hstack((img, mask_out))
#numpy_horizontal_concat = np.concatenate((img, mask_out), axis=1)
plt.imshow(mask_out)
cv2.waitKey(0)
# save the resulting image
cv2.imwrite('whiten_background.jpeg',numpy_horizontal_concat)

foreground = cv2.imread(path)
# Create a Gaussian blur of kernel size 7 for the background image
blurredImage = cv2.GaussianBlur(foreground, (7,7), 0)
# Convert uint8 to float
foreground = foreground.astype(float)
blurredImage = blurredImage.astype(float)
# Create a binary mask of the RGB output map using the threshold value 0
th, alpha = cv2.threshold(np.array(rgb),0,255, cv2.THRESH_BINARY)
# Apply a slight blur to the mask to soften edges
alpha = cv2.GaussianBlur(alpha, (7,7),0)
# Normalize the alpha mask to keep intensity between 0 and 1
alpha = alpha.astype(float)/255
# Multiply the foreground with the alpha matte
foreground = cv2.multiply(alpha, foreground)
# Multiply the background with ( 1 - alpha )
background = cv2.multiply(1.0 - alpha, blurredImage)
# Add the masked foreground and background
outImage = cv2.add(foreground, background)
# Return a normalized output image for display
outImage= outImage
#numpy_horizontal = np.hstack((img, outImage))
#numpy_horizontal_concat = np.concatenate((img, outImage), axis=1)
# Display image
plt.imshow(outImage)
cv2.waitKey(0)
# Save the resulting image
cv2.imwrite('blur_background.png' , outImage)

# Load the foreground input image
foreground = cv2.imread(path)
# Resize image to match shape of R-band in RGB output map
foreground = cv2.resize(foreground, (rgb.shape[1],rgb.shape[0]), interpolation = cv2.INTER_AREA)
# Create a background image by copying foreground and converting into grayscale
background = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
# convert single channel grayscale image to 3-channel grayscale image
background = cv2.cvtColor(background, cv2.COLOR_GRAY2RGB)
# Convert uint8 to float
foreground = foreground.astype(float)
background = background.astype(float)
# Create a binary mask of the RGB output map using the threshold value 0
th, alpha = cv2.threshold(np.array(rgb),0,255, cv2.THRESH_BINARY)
# Apply a slight blur to the mask to soften edges
alpha = cv2.GaussianBlur(alpha, (7,7),0)
# Normalize the alpha mask to keep intensity between 0 and 1
alpha = alpha.astype(float)/255
# Multiply the foreground with the alpha matte
foreground = cv2.multiply(alpha, foreground)
# Multiply the background with ( 1 - alpha )
background = cv2.multiply(1.0 - alpha, background)
# Add the masked foreground and background
outImage = cv2.add(foreground, background)
#numpy_horizontal = np.hstack((img, outImage))
#numpy_horizontal_concat = np.concatenate((img, outImage), axis=1)
# Display image
plt.imshow(outImage)
cv2.waitKey(0)
# Saves the image
cv2.imwrite('colourless_back.png' , outImage)

# Reading  images
#image to place in foregroung (main image)
foreground = cv2.imread(path)
#image to place in background
background = cv2.imread(backpath, cv2.IMREAD_COLOR)
background = cv2.resize(background, (rgb.shape[1],rgb.shape[0]), interpolation = cv2.INTER_AREA)
alpha = rgb
# Convert uint8 to float
foreground = foreground.astype(float)
background = background.astype(float)
# Normalize the alpha mask to keep intensity between 0 and 1
alpha = alpha.astype(float)/255
# Multiply the foreground with the alpha matte
foreground = cv2.multiply(alpha, foreground)
# Multiply the background with ( 1 - alpha )
background = cv2.multiply(1.0 - alpha, background)
# Add the masked foreground and background.
outImage = cv2.add(foreground, background)
# Display image
plt.imshow(outImage)
cv2.waitKey(0)
# Saves image
cv2.imwrite('changed_background' , outImage)
