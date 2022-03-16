# from ffmpy import FFmpeg
# file_name = 'sample-5s'
# media_url = f'uploads/media/{file_name}.mp4'

# ff = FFmpeg(inputs={media_url: None}, outputs={
#             f"uploads/video_thumbs/{file_name}.png": ['-ss', '00:00:4', '-vframes', '1']})

# print(ff.cmd)
# ff.run()

# =================================================================

# from PIL import Image
# file_name = '506285'
# media_url = f'uploads/media/{file_name}.jpg'

# img = Image.open(media_url)
# size = (200, 200)
# img.thumbnail(size)

# img.save(f'uploads/img_thumbs/{file_name}.jpg')
