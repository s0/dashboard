"""
Obtains the artwork for media files

"""

import os

try:
    import mutagen
except ImportError:
    mutagen = None

def get_image(root_dir, path):

    print "get image"

    artwork = None

    if root_dir:
        full_path = os.path.join(root_dir, path)
    else:
        full_path = path

    print "### Path: " + full_path
    print mutagen
    print os.path.isfile(full_path)

    # Try ID3
    if mutagen and os.path.isfile(full_path):
        f = mutagen.File(full_path)
        for t in f.tags:
            print t
        artwork = f.tags['APIC:'].data

    # Try Looking for image files
    if not artwork:
        pass

    if artwork:
        print "ARTWORK!"
        print type(artwork)
        print artwork
