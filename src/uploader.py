from drive_utils import *
from gui import gui


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
