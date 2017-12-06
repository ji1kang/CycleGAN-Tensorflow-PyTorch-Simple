"""Image tiling."""

import os
import glob
from math import sqrt, ceil, floor

from PIL import Image
from PIL import ImageOps


def calc_columns_rows(n):
    """Calculate the number of columns and rows for n parts."""
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)


def join(tile_paths, save_path=None):
    """Join image tiles into one."""
    tile_paths.sort()
    directory = os.path.dirname(tile_paths[0])
    basename = os.path.splitext(os.path.basename(tile_paths[0]))[0]
    format = os.path.splitext(os.path.basename(tile_paths[0]))[1][1:]
    if not save_path:
        save_path = directory

    columns, rows = calc_columns_rows(len(tile_paths))
    ti = Image.open(tile_paths[0])
    tile_w, tile_h = ti.size
    ti.close()
    im_w, im_h = (tile_w*columns, tile_h*rows)
    i = 0
    im = Image.new('RGB', (im_w, im_h), None)
    for pos_x in range(0, im_w - columns, tile_w): # as above.
        for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
            tile = Image.open(tile_paths[i])
            im.paste(tile, (pos_x, pos_y))
            i += 1

    imgpath = os.path.join(save_path, "%s.%s" % (basename, format))
    print "Saving image %s" % (imgpath)
    im.save(imgpath)
    # im.save(imgpath, format)

def joinall(path, save_path=None):
    if not save_path:
        save_path = path
    names = {}
    for img in glob.glob(os.path.join(path,"*.jpg")):
        basename = os.path.splitext(os.path.basename(img))[0]
        parts = basename.split('_')
        pre = "_".join(basename.split('_')[:-2])
        if pre not in names:
            names[pre] = None

    for name in names.keys():
        tiles = glob.glob(os.path.join(path,name+"*.jpg"))
        join(tiles, save_path)



def slice(filename, nTiles, save_path=None, fit_size=None, pattern="image%05d.jpg"):
    """Split an image into a specified number of tiles.
    fit_size ... (w,h) a size tuple
    """
    directory = os.path.dirname(filename)
    basename = os.path.splitext(os.path.basename(filename))[0]
    format = os.path.splitext(os.path.basename(filename))[1][1:]
    if not save_path:
        save_path = directory

    im = Image.open(filename)
    if fit_size:
        im = ImageOps.fit(im, fit_size, method=Image.BICUBIC)

    im_w, im_h = im.size
    columns, rows = calc_columns_rows(nTiles)
    extras = (columns * rows) - nTiles
    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)

            tilename = '{prefix}_{col:02d}_{row:02d}.{ext}'.format(
                        prefix=basename, col=position[0], row=position[1], ext=format)
            tilepath = os.path.join(save_path, tilename)

            print "Saving tile %s" % (tilepath)
            image.save(tilepath)


def sliceall(path, save_path, nTiles, fit_size=None, prefix="img%05d"):
    for i, img in enumerate(glob.glob(os.path.join(path,"*.jpg"))):
        newname = os.path.join(path, (prefix+'.jpg') % (i))
        os.rename(img, newname)
        slice(newname, nTiles=nTiles, save_path=save_path, fit_size=fit_size)
