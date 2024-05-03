import os
import json
import boto3
from moviepy.editor import *

s3 = boto3.client('s3')

def get_input_video_path(event):
    input_video_path = event.get("input_video_path", "s3://sam-app-yours3bucketname-1ufqwrupow4x/demo.mp4")
    bucket_name, key = input_video_path.replace("s3://", "").split("/", 1)
    return bucket_name, key

def get_time_range(event):
    t_start = event.get("t_start", 2)
    t_end = event.get("t_end", 6)
    return t_start, t_end

def get_fps(event):
    fps = event.get("fps", 6)
    return fps

def get_size(event):
    size = event.get("size", 0.3)
    return size


def download_video_from_s3(bucket_name, key):
    local_file_path = f"/tmp/{os.path.basename(key)}"
    s3.download_file(bucket_name, key, local_file_path)
    return local_file_path

def create_gif_from_video(local_file_path, t_start, t_end, fps, size):
    clip = VideoFileClip(local_file_path)
    output_gif_path = "/tmp/gfg_gif.gif"
    clip.subclip(t_start=t_start, t_end=t_end).resize(size).write_gif(output_gif_path, fps=fps)
    return output_gif_path

def upload_gif_to_s3(bucket_name, key, output_gif_path):
    output_key = os.path.splitext(key)[0] + ".gif"
    s3.upload_file(output_gif_path, bucket_name, output_key)
    return f"s3://{bucket_name}/{output_key}"

def lambda_handler(event, context):
    bucket_name, key = get_input_video_path(event)
    t_start, t_end = get_time_range(event)
    fps = get_fps(event)
    size = get_size(event)
    
    local_file_path = download_video_from_s3(bucket_name, key)
    output_gif_path = create_gif_from_video(local_file_path, t_start, t_end, fps, size)
    output_gif_path_s3 = upload_gif_to_s3(bucket_name, key, output_gif_path)
    
    body = json.dumps({"output_gif_path": output_gif_path_s3})
    print(body)
    return {
        "statusCode": 200,
        "body": body
    }