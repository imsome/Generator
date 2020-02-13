import image_slicer
import os

img_name = "max.jpg"
resolve_name = img_name.index(".jpg")
resolve_name = img_name[:resolve_name]

imgs = image_slicer.slice("max.jpg", 12)

path = "C:/Generation/Functions/Face_images/"
try:
    os.mkdir(path+"Images/")
except FileExistsError:
    print("Already have directory")
make_new_photos = path + "Images/"
i = 1
for img in imgs:
    src = path+str(img.filename)
    try:
        os.rename(src, path+"Images/"+str(i)+".jpg")
    except FileExistsError:
        os.remove(path+"Images/"+str(i)+".jpg")
        os.rename(src, path+"Images/"+str(i)+".jpg")
    # os.remove(src)
    # i += 1