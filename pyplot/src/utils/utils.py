import os.path

def root():
    return os.path.abspath(os.path.split(__file__)[0] + '../../../..')

if __name__ == '__main__':
    print root()
