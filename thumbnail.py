from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import av
import math
import datetime
import os

#export PATH="/d/Tools/Anaconda3:$PATH"

max_thumb_witdh = 300
max_thumb_height = 200
min_thumbnails = 20
columns_count = 4
margin = 10
bg_color = (255, 255, 255, 255)
font_color = (0,0,0)
font_file = 'tahomabd.ttf'
font_size = 16
time_size = 16
#time_color = (70, 180, 240)
time_color = (255, 255, 255)
info_height = 110
max_interval = 3*60

caption_font = ImageFont.truetype(font_file, font_size)
time_font = ImageFont.truetype(font_file, time_size)


def get_frames(container, interval):
    frames = []
    index = 0
    first_time = None
    time = None
    for frame in container.decode(video=0):
        if not time:
            time = frame.time
            first_time = time
        if frame.time >= time:
            thumb = frame.to_image()
            thumb.thumbnail((max_thumb_witdh, max_thumb_height))

            frame_time = int(frame.time - first_time)
            print_time(thumb, frame_time)
            frames.append((thumb, frame_time))
            index += 1
            time += interval
    return frames


def print_time(image, time):
    draw = ImageDraw.Draw(image)
    time_str = str(datetime.timedelta(seconds=time))

    x_pos = 10
    y_pos = image.height - 20

    draw.text((x_pos, y_pos), time_str, time_color, font=time_font)


def print_info(image, file_name, caption, duration, size):
    draw = ImageDraw.Draw(image)

    caption = 'Caption: {}'.format(caption)

    duration_str =  'Duration: {}'.format(datetime.timedelta(seconds=duration))

    if size > 1024*1024:
        size_str = 'Size: {} Mb'.format(size//(1024*1024))
    else:
        size_str = 'Size: {} Kb'.format(size // 1024)

    draw.text((10, 10), file_name, font_color, font=caption_font)
    draw.text((10, 35), caption, font_color, font=caption_font)
    draw.text((10, 60), duration_str, font_color, font=caption_font)
    draw.text((10, 85), size_str, font_color, font=caption_font)


def combine_frames(frames, info):
    if len(frames) == 0:
        return None

    filename = info[0]
    caption = info[1]
    duration = info[2]
    size = info[3]

    frame0 = frames[0][0]
    frame_width = frame0.width
    frame_height = frame0.height

    rows_count = int(math.ceil(len(frames) / columns_count))

    img_width = frame_width*columns_count + (columns_count+1)*margin
    img_height = frame_height*rows_count + (rows_count +1)*margin + info_height

    img = Image.new('RGB', (img_width, img_height), bg_color)
    print_info(img, filename, caption, duration, size)

    for i, elem in enumerate(frames):
        (frame, time) = elem
        row_index = i // columns_count
        col_index = i % columns_count
        x_pos = col_index*frame_width + (col_index+1)*margin
        y_pos = row_index*frame_height + (row_index+1)*margin + info_height
        img.paste(frame, (x_pos, y_pos))

    return img


def generate_thumb(input_filename, out_filename, caption='', origin_filename=None):
    container = av.open(input_filename)

    duration = container.duration // 1000000

    #print("video duration: {}".format(duration))

    interval = duration/min_thumbnails
    if interval > max_interval:
        interval = max_interval

    #print("interval = {}".format(interval))

    frames = get_frames(container, interval)

    if not origin_filename:
        origin_filename = input_filename

    size = os.path.getsize(input_filename)

    info = (origin_filename, caption, duration, size)
    img = combine_frames(frames, info)
    img.save(out_filename)

file_path = 'C:\\temp\session5844\\record_1.ts'
generate_thumb(file_path, "out.jpg")