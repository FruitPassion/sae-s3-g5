import os


def get_flat():
    dir_path = 'static/images/flat'
    files = []
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)):
            # add filename to list
            files.append(file_path)
    return files
