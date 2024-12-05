import os

LINUX_MODE = True

if LINUX_MODE:
    paths = [
        "/media/kaczorekt/NIE USUWAJ/Homework",
        "/media/kaczorekt/ChałupaNaDucha/MaxxerPlaylist/To Sort",
        "/media/kaczorekt/Studia/Homework"
    ]
else:
    paths = [
        "F:/MaxxerPlaylist/To Sort",
        "D:/Homework",
        "E:/Homework"
    ]

def search_file(file_prefix):
    found_files = []
    for path in paths:
        for root_dir, _, files in os.walk(path):
            for file in files:
                if file_prefix.lower() in file.lower():
                    found_files.append(os.path.join(root_dir, file))
    return found_files
