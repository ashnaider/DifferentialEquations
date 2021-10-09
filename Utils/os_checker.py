from sys import platform

SLASH = '/'

if platform == "linux" or platform == "linux2":
    # linux
    SLASH = '/'
elif platform == "darwin":
    # OS X
    SLASH = '/'
elif platform == "win32":
    # Windows...
    SLASH = '\\'
