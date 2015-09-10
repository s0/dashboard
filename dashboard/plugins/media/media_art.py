"""
Obtains the artwork for media files

"""

import base64
import os

try:
    import mutagen
except ImportError:
    mutagen = None

def get_image(root_dir, path):

    print "get image"

    artwork = None
    artwork_content_type = "image/jpeg"

    if root_dir:
        full_path = os.path.join(root_dir, path)
    else:
        full_path = path

    # Try ID3
    if mutagen and os.path.isfile(full_path):
       f = mutagen.File(full_path)
       try:
           picture = f.pictures[0]
           artwork = picture.data
           artwork_content_type = picture.mime
       except Exception:
           if 'APIC:' in f.tags:
               artwork = f.tags['APIC:'].data
           if 'covr' in f.tags:
               artwork = f.tags['covr'].data

    # Try Looking for image files
    if not artwork:
        print "artwork not found"

    if artwork:
        return 'data:' + artwork_content_type + ';base64,' + base64.b64encode(artwork)
