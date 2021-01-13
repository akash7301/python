import cv2
import easygui
import numpy
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk,Image

#making the main window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='blue')
label = Label(top, background='#CDCDCD',font=('calibri',20,'bold'))


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    #read the image
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
    #print(originalImage)
    if originalImage is None:
        print("can't find ant image, choose approriate file")
        sys.exit()

    Resized1 = cv2.resize(originalImage, (960,540))
    #plt.imshow(Resized1, cmap='gray')

    #converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    #grayScaleImage = cv2.Canny(originalImage, 100, 70)
    Resized2 = cv2.resize(grayScaleImage, (960,540))
    #plt.imshow(Resized2, cmap='gray')

    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage,3)
    Resized3 = cv2.resize(smoothGrayScale, (960,540))
    #plt.imshow(Resized3,cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 29, 5)
    Resized4 = cv2.resize(getEdge, (960,540))
    #plt.imshow(Resized4, cmap='gray')

    #applying bilateral filter to remove noise
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalImage, 9, 200, 200)
    Resized5 = cv2.resize(colorImage, (960,540))
    #plt.imshow(Resised5, cmap='gray')

    #masking egde image with our 'BEAUTIFY' image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    Resized6 = cv2.resize(cartoonImage, (960,540))
    #plt.imshow(Resised6, cmap='gray')


    #plotting the whole transition
    images = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1,wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')


    #making a save button in the main window
    save1 = Button(top, text='save pencil image', command= lambda: save(Resized4,ImagePath, 1),padx=30,pady=5)
    save1.configure(background='#361456', foreground='white', font=('calibri',10,'bold'))
    save1.pack(side=TOP, pady=50)

    save2 = Button(top, text='save cartoonic image', command= lambda: save(Resized6,ImagePath, 2),padx=30,pady=5)
    save2.configure(background='#360056', foreground='white', font=('calibri',10,'bold'))
    save2.pack(side=TOP, pady=50)

    plt.show()

#functionality to save button
def save(Resized4, ImagePath, flag):
    #saving an image using imwrite
    newName = 'cartoonified_image'
    path1 = os.path.dirname(ImagePath)
    originalName = os.path.splitext(ImagePath)[0]
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, originalName+newName+str(flag)+extension)
    cv2.imwrite(path, cv2.cvtColor(Resized4,cv2.COLOR_RGB2BGR))
    I = 'Image saved by name ' + newName + 'at ' + path
    tk.messagebox.showinfo(title=None, message=I)


#making the cartoonify button in main window
upload = Button(top, text='Cartoonify an Image', command=upload, padx=10,pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri',10,'bold'))
upload.pack(side=TOP, pady=50)



top.mainloop()
# if __name__=='__main__':
#     upload()
