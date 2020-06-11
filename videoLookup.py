import requests
import webbrowser

filePath = r'Database/Images/sampleimg2.png'
searchUrl = 'http://www.google.co.in/searchbyimage/upload'
multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
response = requests.post(searchUrl, files=multipart, allow_redirects=False)
fetchUrl = response.headers['Location']
print(fetchUrl)
webbrowser.open(fetchUrl)