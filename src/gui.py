import threading
from tkinter import *
from PIL import ImageTk, Image
import imageio

import os
from os.path import join


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

    thread = threading.Thread()
    thread_on = False

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
        nonlocal count, thread, thread_on, finished

        name.set('')
        count += 1

        if count >= len(img_list):
            if not finished:
                label.config(image='', text='No more images!')
                finished = True
                return
            else:
                sys.exit(0)

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

    entry = Entry(root, textvariable=name)
    entry.bind('<Return>', submit)
    entry.pack(side=RIGHT)

    # Run GUI
    root.mainloop()
