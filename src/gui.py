import threading
from tkinter import *
from PIL import ImageTk, Image
import imageio

import os
from os.path import join

from drive_utils import *


def gui(src, img_dict, drive):
    """
    Graphical user interface for the application.

    :param src: The source directory from where images are displayed
    :param img_dict: Image dictionary to reference
    :param drive: google drive object
    """
    # Setup
    img_list = os.listdir(src)
    count = 0

    root = Tk()

    left_frame = Frame(root)
    left_frame.pack(side=LEFT)

    right_frame = Frame(root)
    right_frame.pack(side=RIGHT)

    # Image and its label
    img = ImageTk.PhotoImage(Image.open(join(src, img_list[0])))
    label = Label(left_frame, image=img)
    label.pack()

    # Text entry field
    name = StringVar()

    info_msg = Label(right_frame, text='The acronym is new, make sure it\'s right', fg='red')

    thread = threading.Thread()
    thread_on = False

    new_input = False
    finished = False

    def stream_vid(label_obj, vid):
        """
        Streams a video frame by frame in a label Tkinter object

        :param label_obj: Tkinter label
        :param vid: video to stream
        """
        while True:
            for image in vid.iter_data():
                if not thread_on:
                    return

                frame = ImageTk.PhotoImage(Image.fromarray(image))
                label_obj.config(image=frame)
                label_obj.frame_ref = frame

    def submit(event):
        """
        When entry text is submitted, uploads the file to Google Drive according to the input and cycles to the next
        image
        """
        nonlocal count, thread, thread_on, finished, new_input

        # Check if done
        if count >= len(img_list) - 1:
            if not finished:
                label.config(image='', text='No more images!')
                finished = True
                return
            else:
                sys.exit(0)

        # Input processing
        data = name.get()

        if data not in img_dict and not new_input:
            info_msg.pack(side=TOP)
            new_input = True

            return
        elif new_input:
            img_dict[data] = 0
            info_msg.pack_forget()
            new_input = False

        img_dict[data] += 1
        file_name = '{}{}'.format(data, img_dict[data])

        thread = threading.Thread(target=upload_to_folder, args=(join(src, img_list[count]), file_name, drive,
                                                                 img_dict['folder_id']))
        thread.start()

        # After input is processed
        name.set('')
        count += 1

        next_name = img_list[count]

        # if video
        if next_name.split('.')[1] == 'mp4':
            video = imageio.get_reader(join(src, next_name))

            thread = threading.Thread(target=stream_vid, args=(label, video))
            thread_on = True
            thread.start()
            return
        else:
            if thread_on:
                thread_on = False

        next_img = ImageTk.PhotoImage(Image.open(join(src, next_name)))
        label.config(image=next_img)
        label.img_ref = next_img

    entry = Entry(right_frame, textvariable=name)
    entry.bind('<Return>', submit)
    entry.pack(side=BOTTOM)

    # Run GUI
    root.mainloop()
