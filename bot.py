import gtk.gdk
import time
import sys
import os
from gfycat.error import GfycatClientError
from gfycat.client import GfycatClient
import webbrowser
from subprocess import Popen, PIPE
import filecmp
#from images2gif import writeGif
from PIL import Image

def cleanDir():
    os.system("rm pics/*.png")
    os.system("rm pics/*.gif")

def screenshot(filename):
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    print("The size of the window is %d x %d" % sz)
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    if (pb != None):
        pb.save(filename, "png")
        return filename
    else:
        print("Unable to get the screenshot.")

def zoomOut():
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input="keydown Control_L\nkey minus\nkeyup Control_L\n")

def pressRight():
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input="key Right\n")

def fullScreen():
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input="key F11\n")

def openReplay(URL):
    #TODO Regex
    webbrowser.open(URL)

def isSame(file1, file2):
    if None in [file1, file2]:
        print("False")
        return False
    res = filecmp.cmp(file1,file2)
    print(res)
    return res

def crop(path):

    #Crop image based on pixelcolor change
    img = Image.open(path)
    pix = img.load()
    for x in range(0,1919):
        if((pix[x,500]) == (34,34,34)):
            print(x)
            break;
    for y in range(0,1079):
        if((pix[250,y]) == (34,34,34)):
            print(y)
            break;

    cropimage = img.crop((0, 0, x, y))

    #resize image to save space
    cropimage.thumbnail([x/2+x/4,y/2+y/4], Image.ANTIALIAS)
    newPath = path[:path.index(".")] + "_cropped.png"

    cropimage.save(newPath)

    return newPath

def setFocus():
    time.sleep(6)
    zoomOut()
    time.sleep(1)
    zoomOut()
    time.sleep(1)
    zoomOut()
    time.sleep(1)
    zoomOut()
    time.sleep(1)
    zoomOut()

def createGif(pics):
    command = "convert -delay 10 " + (" ").join(pics) + " pics/animation.gif"
    os.system(command)
    return "pics/animation.gif"

def upload(path):
    client = GfycatClient()
    try:
        r = client.upload_from_file(path)
        return r
        
    except GfycatClientError as e:
        print(e.error_message)
        print(e.status_code)
    
def main():
    cleanDir()
    if "-r" in sys.argv:
        openReplay(sys.argv[sys.argv.index("-r")+1])
    else:
        print("Please provide a replay link with -r")
        return

    time.sleep(4)
    if("-f" in sys.argv):
        setFocus()
    
    fullScreen()
    time.sleep(5)
    i = 0
    pics = []
    prevPic = None
    pressRight()
    curPic = screenshot("pics/" + str(i) + ".png")
    pics.append(curPic)
    notSameCount = 0

    while 1:
        #Sometimes steps don't change
        if isSame(prevPic, curPic):
            sameCount += 1
            if sameCount > 3:
                break;
        else:
            sameCount = 0
        i+=1
        prevPic = curPic
        pressRight()
        time.sleep(0.2)
        curPic = screenshot("pics/" + str(i) + ".png")
        pics.append(curPic)

    cropped_pics = []

    for i in pics:
        cropped_pics.append(crop(i))
        os.system("rm " + i)

    gif = createGif(cropped_pics)
    r = upload(gif)
    print(r)
    print("done")
