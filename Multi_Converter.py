from PIL import Image, ImageEnhance
import cv2
import webcolors
from moviepy.editor import *
import os 
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import shutil
def resize():
    img = Image.open('Your_File\\' + Image_name)
    width = 22
    height = 7
    resized_img = img.resize((width, height))
    resized_img.save("For_Convertation\\result_for_image\\result\\preresult.png")
    if rem_trans == "y":
        im = Image.open("For_Convertation\\result_for_image\\result\\preresult.png")
        remove_transparency(im).save("For_Convertation\\result_for_image\\result\\preresult.png")
    #make image more saturated and contrasted 
    if post_effects == "y":
        image = Image.open('For_Convertation\\result_for_image\\result\\preresult.png')
        enh_con = ImageEnhance.Contrast(image)
        contrast = 5
        image_contrasted1 = enh_con.enhance(contrast)
        image_contrasted1.save('For_Convertation\\result_for_image\\result\\preresult.png')
        image = Image.open('For_Convertation\\result_for_image\\result\\preresult.png')
        enh_sat = ImageEnhance.Color(image)
        saturation = enh_sat.enhance(2)
        saturation.save('For_Convertation\\result_for_image\\result\\preresult.png')
    img = Image.open('For_Convertation\\result_for_image\\result\\\preresult.png')
    img.show()
#convert video to a images and save it
def video_to_frames(path):
     videoCapture = cv2.VideoCapture()
     videoCapture.open(path)
     fps = videoCapture.get(cv2.CAP_PROP_FPS) 
     frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
     print("fps=", int(fps), "frames=", int(frames))
     for i in range(int(frames)):
          ret, frame = videoCapture.read()
          cv2.imwrite("For_Convertation\\frames\\%d.jpg"%(i), frame)
#resize video to 22x7
def resize_for_video():
    counter = 0
    
    for i in range(all_samples):
        Image_name = str(counter) + ".jpg"
        img = Image.open('For_Convertation\\frames\\' + Image_name)
        width = 22
        height = 7
        resized_img = img.resize((width, height))
        resized_img.save('For_Convertation\\result_for_video\\\Images\\'+str(counter)+'preresult.jpg')
        if post_effects == "y":
            image = Image.open('For_Convertation\\result_for_video\\\Images\\'+str(counter)+'preresult.jpg')
            enh_con = ImageEnhance.Contrast(image)
            contrast = 5
            image_contrasted1 = enh_con.enhance(contrast)
            image_contrasted1.save('For_Convertation\\result_for_video\\Images\\'+str(counter)+'preresult.jpg')
            image = Image.open('For_Convertation\\result_for_video\\Images\\'+str(counter)+'preresult.jpg')
            enh_sat = ImageEnhance.Color(image)
            saturation = enh_sat.enhance(2)
            saturation.save('For_Convertation\\result_for_video\\Images\\'+str(counter)+'preresult.jpg')
        counter+=1
#Remove transparency(fill alpha channel to a white)
def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]
        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im
#Creating folders
asking = input("First launch?\n1)Yes\n2)No\n")
if asking == "1":
    os.mkdir('For_Convertation') 
    os.mkdir('Your_File')
    os.mkdir("For_Convertation\\frames")
    os.mkdir("For_Convertation\\result_for_image")
    os.mkdir("For_Convertation\\result_for_image\\result")
    os.mkdir("For_Convertation\\result_for_video")
    os.mkdir("For_Convertation\\result_for_video\\Images")
    os.mkdir("For_Convertation\\result_for_video\\Images_e")
    os.symlink('C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight', "Bloody_Light_Folder")

else:
    
    shutil.rmtree("For_Convertation\\frames")
    shutil.rmtree("For_Convertation\\result_for_video")
    shutil.rmtree("For_Convertation\\result_for_image")
    os.mkdir("For_Convertation\\frames")
    os.mkdir("For_Convertation\\result_for_image")
    os.mkdir("For_Convertation\\result_for_image\\result")
    os.mkdir("For_Convertation\\result_for_video")
    os.mkdir("For_Convertation\\result_for_video\\Images")
    os.mkdir("For_Convertation\\result_for_video\\Images_e")

type_of_file = str(input("With what type of file, you want to work?\n1)Video\n2)Image\n"))


#Video
if type_of_file == "1":
    print('Small instruction:\nIn the first paragraph, you must write the name of your image, for example: "MyVideo.mp4"\nIn the next paragraph, you must decide whether you need post-effects or not, thanks to them, the backlight becomes brighter and more saturated.\nAll your files will automatically appear in their respective sections')
    input('press enter to continue')
    filenames_saved = input('Input your keyboard filename: ')
    video = input("Input filename: ")
    post_effects = str(input('Input "y" if you want post-effects(led become more bright): '))

    video_input_path = "Your_File\\" + video
    video_output_path = "Your_File\\preresult.mp4"
    video_output2_path = "For_Convertation\\result_for_video\\videoplayback_lessfps_RESULT.mp4"


    path_to_image_folder = 'For_Convertation\\result_for_video\\\Images'

    clip = ffmpeg_extract_subclip(video_input_path, 0, 10, targetname=video_output_path)
    clip = VideoFileClip(video_output_path)
    clip.write_videofile(video_output2_path, fps=10)
    vid_dur = float(clip.duration)
    all_samples = vid_dur * 10
    all_samples = int(round(all_samples))

    video_to_frames("For_Convertation\\result_for_video\\videoplayback_lessfps_RESULT.mp4")
    resize_for_video()


    color_list = []
    counter1 = 0
    for i in range(all_samples):
        im_cv = cv2.imread('For_Convertation\\result_for_video\\\Images\\'+str(counter1)+'preresult.jpg')
        im_bgr = cv2.cvtColor(im_cv, cv2.COLOR_RGB2BGR)
        cv2.imwrite('For_Convertation\\result_for_video\\\Images_e\\'+str(counter1)+'preresult2.jpg', im_bgr)
        img = Image.open('For_Convertation\\result_for_video\\\Images_e\\'+str(counter1)+'preresult2.jpg')
        g = 1
        j = 1
        while(j < 7):
            if g == 21:
                g = 0
                j+=1
            if j == 7:
                break
            g+=1
            buf = img.getpixel((g, j))
            result = webcolors.rgb_to_hex(buf)
            color_list.append(result)

        color_list = str(color_list)
        color_list = color_list.replace("#", '')
        color_list = color_list.replace("'", '')
        color_list = color_list.replace("[", '')
        color_list = color_list.replace("]", '')
        color_list = color_list.replace(",", '')
        chunks = color_list.split(sep=None, maxsplit=-1)
        del chunks[2]
        del chunks[13:17]
        del chunks[67:70]
        del chunks[71]
        del chunks[71]
        del chunks[82]
        del chunks[82]
        del chunks[83]
        del chunks[91:97]
        color_list = str(chunks)
        color_list = color_list.replace('#', '')
        color_list = color_list.replace("'", '')
        color_list = color_list.replace("[", '')
        color_list = color_list.replace("]", '')
        if counter1 == 0:
            with open("C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\" + str(filenames_saved) + '.ckAnimation', 'w+', encoding = 'utf-16') as f:
                f.write('<?xml version="1.0" encoding="Unicode"?>\n' + '<Root>\n' + '	<Description>ckPannel:\n' + 'Programm was created by SNIP\n' + 'THX FOR USING\n' + '</Description>\n' + '<time>' + '0.1' + '</time>\n' + "<FrameCount>" + str(all_samples-1) + "</FrameCount>\n" + "<Frame" + str(counter1) + ">\n" + "<ColorPicture>" + str(color_list) + "</ColorPicture>\n"  + "<DisplayTime>0.1</DisplayTime>\n"     + "</Frame" + str(counter1) + ">\n")
                f.close()
        elif counter1 == all_samples - 1:
            with open("C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\" + str(filenames_saved) + '.ckAnimation', 'a', encoding = 'utf-16') as f:
                f.write("<Frame" + str(counter1) + ">\n" + "<ColorPicture>" + str(color_list) + "</ColorPicture>\n"  + "<DisplayTime>0.1</DisplayTime>\n" + "</Frame" + str(counter1) + ">\n" + '</Root>\n')
                f.close()
        else:
            with open("C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\" + str(filenames_saved) + '.ckAnimation', 'a', encoding = 'utf-16') as f:
                f.write("<Frame" + str(counter1) + ">\n" + "<ColorPicture>" + str(color_list) + "</ColorPicture>\n"  + "<DisplayTime>0.1</DisplayTime>\n" + "</Frame" + str(counter1) + ">\n")
                f.close()
        counter1+=1
        color_list = []
#Image
elif type_of_file == "2":

    print('Small instruction:\nIn the first paragraph, you must write the name of your image, for example: "MyImage.png"\nIn the next paragraph, you must decide whether you need post-effects or not, thanks to them, the backlight becomes brighter and more saturated.\nIn the last paragraph, you must specify "y", only in this case:\nYou have a png image with an alpha channel (transparency effect), if so, the program will fill the alpha channel with white and the error should disappear.\nAll your files will automatically appear in their respective sections')
    input('press enter to continue')
    filenames_saved = input('Input your keyboard filename: ')
    Image_name = str(input('Input filename: '))
    post_effects = str(input('Input "y" if you want post-effects(led become more bright): '))
    rem_trans = input('Input "y" if you have need to fill Alpha-channel to white: ')

    resize()

    im_cv = cv2.imread('For_Convertation\\result_for_image\\result\\preresult.png')
    im_bgr = cv2.cvtColor(im_cv, cv2.COLOR_RGB2BGR)
    cv2.imwrite('For_Convertation\\result_for_image\\result\\preresult2.png', im_bgr)
    img = Image.open("For_Convertation\\result_for_image\\result\\preresult2.png")
    color_list = []
    g = 1
    j = 1
    while(j < 7):
        if g == 21:
            g = 0
            j+=1
        if j == 7:
            break
        g+=1
        buf = img.getpixel((g, j))
        result = webcolors.rgb_to_hex(buf)
        color_list.append(result)
    color_list = str(color_list)
    color_list = color_list.replace('#', '')
    color_list = color_list.replace("'", '')
    color_list = color_list.replace("[", '')
    color_list = color_list.replace("]", '')
    color_list = color_list.replace(",", '')
    chunks = color_list.split(sep=None, maxsplit=-1)
    del chunks[2]
    del chunks[13:17]
    del chunks[67:70]
    del chunks[71]
    del chunks[71]
    del chunks[82]
    del chunks[82]
    del chunks[83]
    del chunks[91:97]

    color_list = str(chunks)

    color_list = color_list.replace('#', '')
    color_list = color_list.replace("'", '')
    color_list = color_list.replace("[", '')
    color_list = color_list.replace("]", '')
    filenames_saved = filenames_saved.replace(".png", '')
    filenames_saved = filenames_saved.replace(".jpg", '')
    filenames_saved = filenames_saved.replace(".jpeg", '')
    print("Имя вашего файла: " + filenames_saved)
    with open("C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\" + str(filenames_saved) + '.ckPannel', 'w+', encoding = 'utf-16') as f:
        f.write('<?xml version="1.0" encoding="Unicode"?>\n' + '<Root>\n' + '	<Description>ckPannel:\n' + 'Programm was created by SNIP\n' + 'THX FOR USING\n' + '</Description>\n' + '<ColorPicture>' + color_list + '</ColorPicture>\n' + '</Root>\n')
        f.close()

print("Finish, open KeyDominator2, thx for using my programm;)")