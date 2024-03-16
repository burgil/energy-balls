import os
from PIL import Image
import rembg
import cv2

transparentMP4 = False

def remove_background(input_image_path, output_image_path):
    with open(input_image_path, "rb") as input_file:
        input_image = input_file.read()
    output_image = rembg.remove(input_image)
    with open(output_image_path, "wb") as output_file:
        output_file.write(output_image)

def convert_img_to_webp(img_file, webp_file, quality=100):
    im = Image.open(img_file)
    im.save(webp_file, 'WEBP', quality=quality)

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    all_frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        all_frames.append(frame_path)
        print("Extracting Frame For:", video_path, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()
    print("Frames extraction completed successfully.")
    submaxfiles = len(all_frames)
    subcurrentfile = 0
    for sub_single_file in all_frames:
        subcurrentfile = subcurrentfile + 1
        if transparentMP4:
            print("--- Transparent Sub Progress: " + str(format(subcurrentfile/submaxfiles*100, ".2f")) + '%' + ' - ' + str(subcurrentfile) + '/' + str(submaxfiles))
            png_file = sub_single_file.replace('.jpg', '.png')
            remove_background(sub_single_file, png_file)
            webp_file = png_file.replace('.png', '.webp').replace('.PNG', '.webp')
            convert_img_to_webp(png_file, webp_file)
        else:
            print("--- Sub Progress: " + str(format(subcurrentfile/submaxfiles*100, ".2f")) + '%' + ' - ' + str(subcurrentfile) + '/' + str(submaxfiles))
            webp_file = sub_single_file.replace('.jpg', '.webp').replace('.JPG', '.webp')
            convert_img_to_webp(sub_single_file, webp_file)

def find_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

all_files = find_all_files('.')
maxfiles = len(all_files)
currentfile = 0
for single_file in all_files:
    currentfile = currentfile + 1
    print("--- Progress: " + str(format(currentfile/maxfiles*100, ".2f")) + '%' + ' - ' + str(currentfile) + '/' + str(maxfiles))
    if single_file.endswith(".png") or single_file.endswith(".PNG"):
        webp_file = single_file.replace('.png', '.webp').replace('.PNG', '.webp')
        if not os.path.exists(webp_file):
            print('single_file PNG->WEBP', webp_file)
            convert_img_to_webp(single_file, webp_file)
    elif single_file.endswith(".jpg") or single_file.endswith(".JPG"):
        webp_file = single_file.replace('.jpg', '.webp').replace('.JPG', '.webp')
        if not os.path.exists(webp_file):
            print('RESUME MODE - single_file JPG->WEBP', webp_file)
            convert_img_to_webp(single_file, webp_file)
    elif single_file.endswith(".mp4") or single_file.endswith(".MP4"):
        folder_name = os.path.splitext(single_file)[0]
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)
            print('single_file MP4', single_file)
            extract_frames(single_file, folder_name)
    else:
        if not single_file.endswith(".webp") and not single_file.endswith(".WEBP"):
            print('Ignoring single_file', single_file)

print("Finished!")