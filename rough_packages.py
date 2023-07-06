import face_recognition



def frame_definer(target_frame):
    # Convert the BGR frame to RGB for displaying with plt
    face_locations = face_recognition.face_locations(target_frame, model="cnn")

    # Get the image shape
    image_height, image_width, _ = target_frame.shape

    # Iterate over the detected faces
    for face_location in face_locations:
        # Extract the coordinates of the face bounding box
        top, right, bottom, left = face_location

        # Scale the coordinates to match the image shape
        scaled_top = top / image_height
        scaled_right = right / image_width
        scaled_bottom = bottom / image_height
        scaled_left = left / image_width

        # print(scaled_top, scaled_right, scaled_bottom, scaled_left)

        # print((scaled_left + scaled_right) / 2)

        # Calculate center coordinates
        center_x = (scaled_left + scaled_right) / 2
        center_y = (scaled_top + scaled_bottom) / 2

        # Expand rectangle with certain ratio
        expand_width = abs(center_x - scaled_left) * 1.0
        expand_height = abs(center_y - scaled_top) * 1.0 # not use
        expand_top = abs(center_y - scaled_top) * 1.0
        expand_bottom = abs(center_y - scaled_top) * 1.0

        # Crop the face region from the original image
        back_scaled_top = scaled_top - expand_top
        back_scaled_right = scaled_right + expand_width
        back_scaled_bottom = scaled_bottom + expand_bottom
        back_scaled_left = scaled_left - expand_width


        back_scaled_top = int(back_scaled_top*image_height)
        back_scaled_right = int(back_scaled_right*image_width)
        back_scaled_bottom = int(back_scaled_bottom*image_height)
        back_scaled_left = int(back_scaled_left*image_width)

#         print(back_scaled_top, back_scaled_right, back_scaled_left ,back_scaled_left)

#         face_image = image[back_scaled_top:back_scaled_bottom,
#                            back_scaled_left:back_scaled_right]
    # return center_x*image_width, center_y*image_height
    return back_scaled_top, back_scaled_right, back_scaled_bottom, back_scaled_left


# import argparse
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from pydub.utils import mediainfo


os.makedirs("./output", exist_ok=True)

# parser = argparse.ArgumentParser(description="This is a source video cropper.")

# parser.add_argument('--video', dest='video_input', type=str, required=True, help='input video file path to be cropped.')
# parser.add_argument('--audio', dest='audio_input', type=str, default='./output/tts_audio.wav', help='input audio file for the video. it decides the length of the video.')
# parser.add_argument('--output', dest='video_output', type=str, default='./output/cropped_video.mp4', help='output file path of the cropped video.')
# parser.add_argument('--fps', dest='video_fps', type=int, default=30, help='fps of the cropped video.')
# parser.add_argument('--resolution', dest='video_res', type=int, default=256, help='resolution x resolution, 256 for vox.')

# args = parser.parse_args()

def source_video_cropper(video_input:str, audio_input:str='./output/tts_audio.wav',
                        video_output:str='./output/cropped_video.mp4', video_fps:int=30,
                        video_res:int=256):
    audio_info = mediainfo(audio_input)
    audio_duration = float(audio_info['duration'])

    # Write the video clip
    video_clip = VideoFileClip(video_input).subclip(0, audio_duration)
    modified_clip = video_clip.set_fps(video_fps) # set fps == 30
    # modified_clip.write_videofile(args.video_output)

    # Capture the first frame
    first_frame = modified_clip.get_frame(0)

    # back_scaled_top, back_scaled_right, back_scaled_bottom, back_scaled_left
    crop_y1, crop_x2, crop_y2, crop_x1 = frame_definer(first_frame)

    # crop and resize
    cooked_video = modified_clip.crop(x1=crop_x1, x2=crop_x2, y1=crop_y1, y2=crop_y2)

    if os.path.exists(video_output):
        os.remove(video_output)
    cooked_video.write_videofile(video_output, temp_audiofile=False)

def final_video_maker(video_input:str='./output/face_sync.mp4', audio_input:str='./output/tts_audio.wav',
                    video_output:str='./output/face_sync_final.mp4'):
    
    audio_info = mediainfo(audio_input) #ffmpeg required

    audio_duration = float(audio_info['duration'])

    video_clip = VideoFileClip(video_input).subclip(0, audio_duration)

    video_clip.write_videofile(video_output)

