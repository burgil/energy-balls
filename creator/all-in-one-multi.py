import os
from PIL import Image
import rembg
import cv2
import concurrent.futures

maxfiles = 0
currentfile = 0
transparentMP4 = False
currentdir = os.getcwd()

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

def find_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def process_file(single_file):
    global currentfile
    currentfile += 1
    prog = "--- Progress: " + str(format(currentfile/maxfiles*100, ".2f")) + '%' + ' - ' + str(currentfile) + '/' + str(maxfiles)
    # print(prog)
    os.system("title all-in-one-multi " + currentdir + ' ' + prog)
    if single_file.endswith(".png") or single_file.endswith(".PNG"):
        webp_file = single_file.replace('.png', '.webp').replace('.PNG', '.webp')
        if not os.path.exists(webp_file):
            # a=1
            print('single_file PNG->WEBP', webp_file)
            convert_img_to_webp(single_file, webp_file)
        else:
            try:
                file_stats = os.stat(webp_file)
                if file_stats.st_size < 1024:
                    print("Found Corrupted Image! Rebuilding A1!", webp_file)
                    os.remove(webp_file)
                    print('single_file PNG->WEBP', webp_file)
                    convert_img_to_webp(single_file, webp_file)
            except Exception as e:
                print("Found Corrupted Image! Rebuilding A2!", webp_file, e)
                os.remove(webp_file)
                print('single_file PNG->WEBP', webp_file)
                convert_img_to_webp(single_file, webp_file)
    elif single_file.endswith(".jpg") or single_file.endswith(".JPG"):
        png_file = single_file.replace('.jpg', '.png')
        webp_file = png_file.replace('.png', '.webp').replace('.PNG', '.webp')
        if not os.path.exists(png_file):
            # a=1
            print('RESUME MODE - single_file JPG->PNG', png_file)
            remove_background(single_file, png_file)
            print('RESUME MODE - single_file PNG->WEBP', webp_file)
            convert_img_to_webp(png_file, webp_file)
        elif not os.path.exists(webp_file):
            try:
                file_stats = os.stat(png_file)
                if file_stats.st_size < 1024:
                    print("Found Corrupted Image! Rebuilding B1!", png_file)
                    os.remove(png_file)
                    print('RESUME MODE - single_file JPG->PNG', png_file)
                    remove_background(single_file, png_file)
            except Exception as e:
                print("Found Corrupted Image! Rebuilding B2!", png_file, e)
                os.remove(png_file)
                print('RESUME MODE - single_file JPG->PNG', png_file)
                remove_background(single_file, png_file)
            print('RESUME MODE - single_file PNG->WEBP', webp_file)
            convert_img_to_webp(png_file, webp_file)
        else:
            try:
                file_stats = os.stat(png_file)
                if file_stats.st_size < 1024:
                    print("Found Corrupted Image! Rebuilding C1!", png_file)
                    os.remove(png_file)
                    print('RESUME MODE - single_file JPG->PNG', png_file)
                    remove_background(single_file, png_file)
                    print('RESUME MODE - single_file PNG->WEBP', webp_file)
                    convert_img_to_webp(png_file, webp_file)
                else:
                    img = Image.open(png_file)
                    img.verify()
                    img.close()
            except Exception as e:
                print("Found Corrupted Image! Rebuilding C22!", png_file, e)
                os.remove(png_file)
                print('RESUME MODE - single_file JPG->PNG', png_file)
                remove_background(single_file, png_file)
                print('RESUME MODE - single_file PNG->WEBP', webp_file)
                convert_img_to_webp(png_file, webp_file)
            try:
                file_stats = os.stat(webp_file)
                if file_stats.st_size < 1024:
                    print("Found Corrupted Image! Rebuilding D1!", webp_file)
                    os.remove(webp_file)
                    print('RESUME MODE - single_file PNG->WEBP', webp_file)
                    convert_img_to_webp(png_file, webp_file)
            except Exception as e:
                print("Found Corrupted Image! Rebuilding D2!", webp_file, e)
                os.remove(webp_file)
                print('RESUME MODE - single_file PNG->WEBP', webp_file)
                convert_img_to_webp(png_file, webp_file)
    elif single_file.endswith(".mp4") or single_file.endswith(".MP4"):
        folder_name = os.path.splitext(single_file)[0]
        if not os.path.exists(folder_name):
            # a=1
            os.makedirs(folder_name, exist_ok=True)
            print('single_file MP4', single_file)
            extract_frames(single_file, folder_name)
    else:
        if not single_file.endswith(".webp") and not single_file.endswith(".WEBP"):
            print('Ignoring single_file', single_file)

if __name__ == "__main__":
    all_files = find_all_files('.')
    maxfiles = len(all_files)
    currentfile = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(process_file, all_files)
    print("Finished!")
