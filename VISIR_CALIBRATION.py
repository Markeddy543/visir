"""This file takes all the raw images from the VISIR instrument
 and spits out two final 360x360 images at wavelengths 8.9micrometres,
 and 11.7 micrometres, using the chopping and nodding technique, 
 for images of dimensions 900x1024. There were 48 images taken at 11.7 micrometres
 and 40 images taken at 8.9 micrometres"""

import os

from astropy.io import fits
import numpy as np
#Specify path to the directory where the VISIR files are stored
path = "/import/pendragon1/snert/han/VISIR/"
#Open and store all the VISIR image files
files = []

for filename in os.listdir(path):
    if filename.startswith('VISIR_IMG_OBS'):
        files.append(filename)
    

files.sort()
print (files)

#opening the flat file that was made in Making_flats.py
flat_file = fits.open(path+"Making_flat.fits")
f = flat_file[0].data

flat_file.close()


#Chopping and nodding the images
images = []

for i in range (int(len(files)/2)):
    a_file = fits.open(path+files[2 * i])
    b_file = fits.open(path+files[2 * i + 1])
    
    nodA = a_file[3].data
    nodB = b_file[3].data
    
    a_file.close()
    b_file.close()
    
    image = (nodA - nodB)/f
    images.append(image)
    

# hdu = fits.PrimaryHDU(images)
# hdu.writeto('VISIR_INTERMEDIATE_1.fits')
#Testing for a single data pointr

#After chopping and nodding the image needs to be extracted and re-centred

z = len(images)
y = len(images[0])
#x = len(images[0][0])

#dimensions of the final image
d = int(y / 5)
#half_y = int(y / 2)

#Array for the positive and negatives of the chopped and nodded images
pos = np.zeros((2*z,2*d,2*d))
neg = np.zeros((2*z,2*d,2*d))

               
"""Finding the brightest and darkest spots and cutting a 360x360 image out
   and storing them in pos and neg"""     
for k in range(z):
    image = images[k]
    min = 10000000000
    max = -10000000000
    c_min = [0,0]
    c_max = [0,0]
    
    for j in range(y):
        for i in range(150,400):
            if image[j,i] > max:
                max = image[j,i]
                c_max[0] = j
                c_max[1] = i
            if image[j,i] < min:
                min = image[j,i]
                c_min[0] = j
                c_min[1] = i
      
    pos_image = image[c_max[0]-d:c_max[0]+d,c_max[1]-d:c_max[1]+d]
    neg_image = image[c_min[0]-d:c_min[0]+d,c_min[1]-d:c_min[1]+d]
    
    pos[2*k] = pos_image
    neg[2*k] = neg_image
    
    for j in range(y):
        for i in range(500,750):
            if image[j,i] > max:
                max = image[j,i]
                c_max[0] = j
                c_max[1] = i
            if image[j,i] < min:
                min = image[j,i]
                c_min[0] = j
                c_min[1] = i
    
    pos_image = image[c_max[0]-d:c_max[0]+d,c_max[1]-d:c_max[1]+d]
    neg_image = image[c_min[0]-d:c_min[0]+d,c_min[1]-d:c_min[1]+d]
    
    pos[2*k+1] = pos_image
    neg[2*k+1] = neg_image
    
   # print (k)




# hdupos = fits.PrimaryHDU(pos)
# hdupos.writeto('A_VISIR_INTERMEDIATE_POS.fits')

# hduneg = fits.PrimaryHDU(neg)
 #hduneg.writeto('A_VISIR_INTERMEDIATE_NEG.fits')

#Summing over the positive images and then subtracting the sum of all the negative images
 #Need to chnage the numbers depending on the number of files at different wavelengths
image18 = sum(pos[:48],0) - sum(neg[:48],0)
image31 = sum(pos[48:],0) - sum(neg[48:],0)
#finalimage = sum(pos,0) - sum(neg,0)



#Saving the final images
hdu18 = fits.PrimaryHDU(image18)
hdu18.writeto('AA_FINAL_IMAGE_18.fits')


hdu31 = fits.PrimaryHDU(image31)
hdu31.writeto('AA_FINAL_IMAGE_31.fits')

#hdu = fits.PrimaryHDU(finalimage)
#hdu.writeto('A_FINAL_IMAGE2.fits')





