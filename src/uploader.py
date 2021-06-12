from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from tkinter import *
from PIL import ImageTk, Image

import os
from os.path import join


def drive_auth():
    g_auth = GoogleAuth()
    g_auth.LocalWebserverAuth()

    return GoogleDrive(g_auth)


def get_drive_dict(folder_id, drive):
    """
    Returns a dictionary of how many files of each acronym are in the folder

    :param folder_id: ID of folder to parse
    :param drive: Google Drive authenticated object
    """
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()

    drive_dict = dict()

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


def gui(src, img_dict):
    """
    Graphical user interface for the application.

    :param src: The source directory from where images are displayed
    :param img_dict: Image dictionary to reference
    """
    # Setup
    img_list = os.listdir(src)

    root = Tk()

    # Canvas
    canvas = Canvas(root, width=1000, height=2000, confine=False)
    canvas.pack()

    # Image
    img = ImageTk.PhotoImage(Image.open(join(src, img_list[0])))
    canvas.create_image(0, 0, anchor=NW, image=img)

    # Text entry field
    name = StringVar()

    def submit(event):
        name.set('')

    entry = Entry(root, textvariable=name)
    entry.bind('<Return>', submit)

    canvas.create_window(100, 100, window=entry)

    # Run GUI
    root.mainloop()


def main():
    """
    Main function.
    """
    drive = drive_auth()
    drive_dict = get_drive_dict('1vulvrH-jDxUExFd0MPgPhZMPcDJGFzEm', drive)

    src = r'D:\Downloads\Images'

    print(drive_dict)

    # gui(src, drive_dict)


if __name__ == '__main__':
    main()
