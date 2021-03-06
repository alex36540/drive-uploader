from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def drive_auth():
    """
    Authenticates Google Drive
    """
    g_auth = GoogleAuth()
    g_auth.LocalWebserverAuth()

    return GoogleDrive(g_auth)


def get_drive_dict(folder_id, drive):
    """
    Returns a dictionary of how many files of each acronym are in the folder. The folder ID is also contained in the
    dictionary.

    :param folder_id: ID of folder to parse
    :param drive: Google Drive authenticated object
    """
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()

    drive_dict = dict()
    drive_dict['folder_id'] = folder_id

    for file in file_list:
        if file['mimeType'] != 'application/vnd.google-apps.folder':
            title = file['title'].split('.')[0]
            num_index = 0

            # find the first number in the title and split
            while title[num_index].isalpha():
                num_index += 1

            acronym = title[:num_index]
            count = int(title[num_index:])

            # insert value in dictionary accordingly
            if acronym in drive_dict:
                if drive_dict[acronym] < count:
                    drive_dict[acronym] = count
            else:
                drive_dict[acronym] = count

    return drive_dict


def upload_to_folder(src_file, file_name, drive, folder_id):
    """
    Uploads a file to Google Drive folder

    :param src_file: the file to upload
    :param file_name: the new name for the file
    :param drive: google drive object
    :param folder_id: id of the folder to upload to
    """

    file = drive.CreateFile({'title': file_name,
                             'parents': [{'id': folder_id}]
                             })
    file.SetContentFile(src_file)
    file.Upload()

    print('Uploaded ' + file_name)
