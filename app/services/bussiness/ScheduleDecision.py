async def cal_body_fat_detection(img):
    contents = await img.read()  # Read the file content
    filename = img.filename
    content_type = img.content_type
