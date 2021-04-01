import os, requests, json, pyimgur

def uploadAndGetPhoto(photorequesturl):
    photoresponse =  json.loads(requests.get(photorequesturl).content.decode())
    file_path = photoresponse['result']['file_path']
    # when error 404?
    photorequesturl = 'https://api.telegram.org/file/bot{}/{}'.format(os.getenv("TELEGRAM_TOKEN"), file_path)
    print('get photo with get request: {}'.format(photorequesturl))
    photo = requests.get(photorequesturl).content
    
    fp = open("tmpphoto.png", "wb")
    fp.write(photo)
    fp.close()
    
    CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
    PATH = "tmpphoto.png"
    title = "Uploaded with PyImgur"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    return uploaded_image.link
