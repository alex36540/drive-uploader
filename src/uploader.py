from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

g_auth = GoogleAuth()
g_auth.LocalWebserverAuth()
drive = GoogleDrive(g_auth)

img_set = set()

fileList = drive.ListFile({'q': "'1vulvrH-jDxUExFd0MPgPhZMPcDJGFzEm' in parents and trashed=false"}).GetList()

for file in fileList:
    if file['mimeType'] != 'application/vnd.google-apps.folder':
        print('Title: %s, ID: %s' % (file['title'], file['id']))
