from moviepy.video.io.VideoFileClip import VideoFileClip

def convert_video_to_audio(input_video_path, output_audio_path):
    video_clip = VideoFileClip(input_video_path)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_audio_path, codec='mp3')

    # Close the video and audio clips
    audio_clip.close()
    video_clip.close()

# Replace 'input_video.mp4' and 'output_audio.mp3' with your file paths
input_video_path = 'sample.mp4'
output_audio_path = 'sample_output.mp3'

convert_video_to_audio(input_video_path, output_audio_path)
