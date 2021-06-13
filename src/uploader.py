from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from tkinter import *
from PIL import ImageTk, Image
import imageio

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
    count = 0

    root = Tk()

    # Image and its label
    img = ImageTk.PhotoImage(Image.open(join(src, img_list[0])))
    label = Label(root, image=img)
    label.pack(side=LEFT)

    # Text entry field
    name = StringVar()

    def submit(event):
        nonlocal count

        name.set('')
        count += 1

        next_name = img_list[count]

        # if it's a video
        if next_name.split('.')[1] == 'mp4':
            video = imageio.get_reader(img)

        next_img = ImageTk.PhotoImage(Image.open(join(src, next_name)))
        label.config(image=next_img)
        label.img_ref = next_img

    entry = Entry(root, textvariable=name)
    entry.bind('<Return>', submit)
    entry.pack(side=RIGHT)

    # Run GUI
    root.mainloop()


def main():
    """
    Main function.
    """
    # drive = drive_auth()
    drive_dict = None  # get_drive_dict('1vulvrH-jDxUExFd0MPgPhZMPcDJGFzEm', drive)

    src = r'D:\Downloads\Images'

    gui(src, drive_dict)


if __name__ == '__main__':
    main()
