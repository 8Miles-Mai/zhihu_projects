__author__ = 'miles'

def write_file(file, data):
    if(data is None or len(data) <= 0):
        return
    file_object = open(file, 'w')
    try:
        file_object.writelines(data)
    except Exception, e:
        print(e)
    finally:
        file_object.close()

def read_file(file):
    data = []
    if file is None:
        return data
    try:
        input_file = open(file)
        for line in input_file:
            data.append(line)
    except Exception, e:
        print e
        data = []
    return data