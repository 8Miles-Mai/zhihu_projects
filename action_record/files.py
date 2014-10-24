__author__ = 'miles'

def write_file(file, data):
    if(data is None or len(data) <= 0):
        return
    file_object = open(file, 'w')
    try:
        file_object.writelines(data)
    finally:
        file_object.close()
