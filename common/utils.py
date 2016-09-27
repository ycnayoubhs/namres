def __open_to_read(name):
    try:
        # for python 3.x
        return open(name, 'r', encoding='utf-8')
    except TypeError:
        # for python2.7
        return open(name, 'r')
