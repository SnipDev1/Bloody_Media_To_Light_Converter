import os
import art
import cv2
import sys
import shutil
import platform
import webcolors
import msvcrt
from pathlib import Path
from PIL import Image, ImageEnhance
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']
SUPPORTED_VIDEO_FORMATS = ['.mp4']


def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]
        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        bg = Image.new('RGBA', im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im


def video_to_frames(path):
    video_capture = cv2.VideoCapture()
    video_capture.open(path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print('fps=', int(fps), 'frames=', int(frames))
    for i in range(int(frames)):
        ret, frame = video_capture.read()
        cv2.imwrite('For_Convertation\\frames\\%d.jpg' % (i), frame)


def resize(image_name: str, use_post_effects: bool, rem_trans: bool):
    img = Image.open(image_name)
    preresult_path = 'For_Convertation\\result_for_image\\result\\preresult.png'
    width = 22
    height = 7
    resized_img = img.resize((width, height))
    resized_img.save(preresult_path)
    if rem_trans:
        im = Image.open(preresult_path)
        remove_transparency(im).save(preresult_path)
    # make image more saturated and contrasted
    if use_post_effects:
        image = Image.open(preresult_path)
        enh_con = ImageEnhance.Contrast(image)
        contrast = 5
        image_contrasted1 = enh_con.enhance(contrast)
        image_contrasted1.save(preresult_path)
        image = Image.open(preresult_path)
        enh_sat = ImageEnhance.Color(image)
        saturation = enh_sat.enhance(2)
        saturation.save(preresult_path)
    img = Image.open(preresult_path)
    img.show()


def resize_for_video(samples: int, use_post_effects: bool):
    counter = 0
    for i in range(samples):
        image_name = f'{counter}.jpg'
        preresult_path = f'For_Convertation\\result_for_video\\\Images\\{str(counter)}preresult.jpg'
        img = Image.open(f'For_Convertation\\frames\\{image_name}')
        width = 22
        height = 7
        resized_img = img.resize((width, height))
        resized_img.save(preresult_path)
        if use_post_effects:
            image = Image.open(preresult_path)
            enh_con = ImageEnhance.Contrast(image)
            contrast = 5
            image_contrasted1 = enh_con.enhance(contrast)
            image_contrasted1.save(preresult_path)
            image = Image.open(preresult_path)
            enh_sat = ImageEnhance.Color(image)
            saturation = enh_sat.enhance(2)
            saturation.save(preresult_path)
        counter += 1


def main():
    art.tprint('BMLC')
    print('Bloody Media to Light Converter by SNIP\n')

    if platform.system() != 'Windows':
        print('The software can only run on Windows.')
        msvcrt.getch()
        return

    if not os.path.exists('C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight'):
        print('KeyDominator2 is not installed.')
        msvcrt.getch()
        return

    Path('Output').mkdir(parents=True, exist_ok=True)
    Path('For_Convertation').mkdir(parents=True, exist_ok=True)
    Path('For_Convertation\\result_for_image').mkdir(parents=True, exist_ok=True)
    Path('For_Convertation\\result_for_image\\result').mkdir(parents=True, exist_ok=True)
    Path('For_Convertation\\result_for_video').mkdir(parents=True, exist_ok=True)
    Path('For_Convertation\\result_for_video\\Images').mkdir(parents=True, exist_ok=True)
    Path('For_Convertation\\result_for_video\\Images_e').mkdir(parents=True, exist_ok=True)

    file_name: str

    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = input('Input file name (with file extension): ')

    file_path = Path(file_name)

    file_type: str

    if not file_path.is_file():
        print('No file with such name.')
        shutil.rmtree('For_Convertation')
        shutil.rmtree('Output')
        msvcrt.getch()
        return

    print(f'Selected file: {file_name}')

    if file_path.suffix in SUPPORTED_IMAGE_FORMATS:
        file_type = 'image'
    elif file_path.suffix in SUPPORTED_VIDEO_FORMATS:
        file_type = 'video'
    else:
        print('Unsupported file type.')
        shutil.rmtree('For_Convertation')
        shutil.rmtree('Output')
        msvcrt.getch()
        return

    filenames_saved = input('Input your keyboard filename: ')

    if file_type == 'video':
        post_effects = input('Input "y" if you want post-effects (led become more bright): ') == 'y'

        video_output_path = 'Output\\preresult.mp4'
        video_output2_path = 'For_Convertation\\result_for_video\\videoplayback_lessfps_RESULT.mp4'

        # Зачем приравнивать clip к функции которая возвращает None?
        clip = ffmpeg_extract_subclip(file_name, 0, 10, targetname=video_output_path)
        clip = VideoFileClip(video_output_path)
        clip.write_videofile(video_output2_path, fps=10)
        vid_dur = float(clip.duration)
        all_samples = vid_dur * 10
        all_samples = int(round(all_samples))

        video_to_frames('For_Convertation\\result_for_video\\videoplayback_lessfps_RESULT.mp4')
        resize_for_video(all_samples, post_effects)

        color_list = []
        counter1 = 0
        for i in range(all_samples):
            im_cv = cv2.imread('For_Convertation\\result_for_video\\\Images\\'+str(counter1)+'preresult.jpg')
            im_bgr = cv2.cvtColor(im_cv, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'For_Convertation\\result_for_video\\\Images_e\\{str(counter1)}preresult2.jpg', im_bgr)
            img = Image.open(f'For_Convertation\\result_for_video\\\Images_e\\{str(counter1)}preresult2.jpg')
            g = 1
            j = 1
            while (j < 7):
                if g == 21:
                    g = 0
                    j += 1
                if j == 7:
                    break
                g += 1
                buf = img.getpixel((g, j))
                result = webcolors.rgb_to_hex(buf)
                color_list.append(result)

            color_list = str(color_list)
            color_list = color_list.replace('#', '')
            color_list = color_list.replace('\'', '')
            color_list = color_list.replace('[', '')
            color_list = color_list.replace(']', '')
            color_list = color_list.replace(',', '')
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
            color_list = color_list.replace('\'', '')
            color_list = color_list.replace('[', '')
            color_list = color_list.replace(']', '')
            if counter1 == 0:
                with open('C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\' + str(filenames_saved) + '.ckAnimation', 'w+', encoding='utf-16') as f:
                    f.write('<?xml version="1.0" encoding="Unicode"?>\n' + '<Root>\n' + '	<Description>ckPannel:\n' + 'Programm was created by SNIP\n' + 'THX FOR USING\n' + '</Description>\n' + '<time>' + '0.1' + '</time>\n' + '<FrameCount>' +
                            str(all_samples-1) + '</FrameCount>\n' + '<Frame' + str(counter1) + '>\n' + '<ColorPicture>' + str(color_list) + '</ColorPicture>\n' + '<DisplayTime>0.1</DisplayTime>\n' + '</Frame' + str(counter1) + '>\n')
                    f.close()
            elif counter1 == all_samples - 1:
                with open('C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\' + str(filenames_saved) + '.ckAnimation', 'a', encoding='utf-16') as f:
                    f.write('<Frame' + str(counter1) + '>\n' + '<ColorPicture>' + str(color_list) + '</ColorPicture>\n' +
                            '<DisplayTime>0.1</DisplayTime>\n' + '</Frame' + str(counter1) + '>\n' + '</Root>\n')
                    f.close()
            else:
                with open('C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\' + str(filenames_saved) + '.ckAnimation', 'a', encoding='utf-16') as f:
                    f.write('<Frame' + str(counter1) + '>\n' + '<ColorPicture>' + str(color_list) +
                            '</ColorPicture>\n' + '<DisplayTime>0.1</DisplayTime>\n' + '</Frame' + str(counter1) + '>\n')
                    f.close()
            counter1 += 1
            color_list = []
    else:
        post_effects = str(input('Input "y" if you want post-effects (led become more bright): ')) == 'y'
        rem_trans = input('Input "y" if you have need to fill Alpha-channel to white: ') == 'y'

        resize(file_name, post_effects, rem_trans)

        im_cv = cv2.imread('For_Convertation\\result_for_image\\result\\preresult.png')
        im_bgr = cv2.cvtColor(im_cv, cv2.COLOR_RGB2BGR)
        cv2.imwrite('For_Convertation\\result_for_image\\result\\preresult2.png', im_bgr)
        img = Image.open('For_Convertation\\result_for_image\\result\\preresult2.png')
        color_list = []
        g = 1
        j = 1
        while (j < 7):
            if g == 21:
                g = 0
                j += 1
            if j == 7:
                break
            g += 1
            buf = img.getpixel((g, j))
            result = webcolors.rgb_to_hex(buf)
            color_list.append(result)
        color_list = str(color_list)
        color_list = color_list.replace('#', '')
        color_list = color_list.replace('\'', '')
        color_list = color_list.replace('[', '')
        color_list = color_list.replace(']', '')
        color_list = color_list.replace(',', '')
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
        color_list = color_list.replace('\'', '')
        color_list = color_list.replace('[', '')
        color_list = color_list.replace(']', '')
        filenames_saved = filenames_saved.replace('.png', '')
        filenames_saved = filenames_saved.replace('.jpg', '')
        filenames_saved = filenames_saved.replace('.jpeg', '')
        print('Output file name: ' + filenames_saved)
        with open('C:\\Program Files (x86)\\KeyDominator2\\KeyDominator2\\Data\\Keyboard\\English\\SLED\\NumberPadAtRight\\' + str(filenames_saved) + '.ckPannel', 'w+', encoding='utf-16') as f:
            f.write('<?xml version="1.0" encoding="Unicode"?>\n' + '<Root>\n' + '	<Description>ckPannel:\n' + 'Programm was created by SNIP\n' +
                    'THX FOR USING\n' + '</Description>\n' + '<ColorPicture>' + color_list + '</ColorPicture>\n' + '</Root>\n')
            f.close()
    shutil.rmtree('For_Convertation')
    shutil.rmtree('Output')
    print("Finish, open KeyDominator2, thx for using my programm ;)")


if __name__ == '__main__':
    main()
