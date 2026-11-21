import cfg
import dxf
import elr
import cir
import gds
import pad


def srect(x, y, length, width):
  dxf.srect('edge', x, y, length, cfg.eg)
  return dxf.srect('core', x, y, length, width)


def sline(x, y, length):
  dxf.srect('edge', x, y, length, cfg.eg)
  return dxf.srect('core', x, y, length, cfg.wg)


def tline(x, y, length):
  w, d, dy = cfg.wg * 0.5, cfg.eg * 0.5, y + length
  dxf.crect('edge', x - d, y, x + d, dy)
  dxf.crect('core', x - w, y, x + w, dy)
  return x, dy


def tilts(x, y, length, wg, angle):
  dxf.tilts('edge', x, y, length, cfg.eg, angle)
  return dxf.tilts('core', x, y, length, wg, angle)


def taper(x, y, length, wstart, wstop):
  dxf.srect('edge', x, y, length, cfg.eg)
  return dxf.taper('core', x, y, length, wstart, wstop)


def bends(x, y, angle, rotate, xsign, ysign):
  layers = {'core': cfg.wg, 'edge': cfg.eg}
  x1, y1 = x, y
  for layer, width in layers.items():
    df = elr.curve(width, cfg.radius, angle, cfg.draft)
    x1, y1 = dxf.bends(layer, df, x, y, rotate, xsign, ysign)
  return x1, y1


def sbend(x, y, angle, dy):
  layers = {'core': cfg.wg, 'edge': cfg.eg}
  x1, y1 = x, y
  for layer, width in layers.items():
    df = elr.curve(width, cfg.radius, angle, cfg.draft)
    x1, y1 = dxf.sbend(layer, df, x, y, dy)
  return x1, y1


def electrode(x, y, sign):
  pad.electrode('metal', x, y, cfg.lpad, 6, sign)
  pad.electrode('edge', x, y, cfg.lpad, cfg.eg, sign)


def texts(x, y, title, scale, align):
  xs = {'r': -1, 'l': 1, 'c':1}
  ys = {'t': -50, 'b': 50, 'c':0}
  xsign = xs[align[0]]
  ysign = ys[align[1]]
  d = 10 * scale * 2  # 10 when scale = 0.5
  dx, dy = dxf.texts('core', x + xsign * d, y, title, scale, align)
  x = x - dx * 0.5 if 'c' in align[0] else x
  dxf.srect('edge', x, y + ysign * scale, xsign * (dx + d * 2), dy + 10)


def marks(layer, x, y):
  dl = 150
  dx = x + cfg.lchip
  dy = y + cfg.lchip
  dxf.triangle(layer, x, y, x + dl, y, x, y + dl)
  dxf.triangle(layer, dx, y, dx - dl, y, dx, y + dl)
  dxf.triangle(layer, x, dy, x + dl, dy, x, dy - dl)
  dxf.triangle(layer, dx, dy, dx - dl, dy, dx, dy - dl)


def filled(x, y):
  dxf.crect('rect', x, y, x + cfg.lsize, y + cfg.lsize)
  marks('edge', x, y)
  return x, y


def split(layer, xpos, ypos):
  dxf.split(layer, xpos * cfg.skey, ypos * cfg.skey)


def euler(wg, radius, angle):
  return elr.curve(wg, radius, angle, cfg.draft)


def circular(wg, radius, angle):
  return cir.curve(wg, radius, angle, cfg.draft)


def savedxf(filename):
  print(f'Saving ... {filename}.dxf')
  dxf.saveas(f'{cfg.path}/{filename}')


def dxf2gds(filename):
  print(f'{filename}.gds to a DXF file')
  gds.dxf2gds(f'{cfg.path}/{filename}')


def saveas(filename):
  print(f'Saving ... {filename}.gds')
  gds.saveas(f'{cfg.path}/{filename}', cfg.layers)


def dlayers(filename, label1, label2):
  print(f'Writing a difference(#{label1} - #{label2}) on #{label2}')
  gds.dlayers(f'{cfg.path}/{filename}', cfg.layers, label1, label2)


def gdstext(filename):
  print('Inserting text')
  gds.texts(f'{cfg.path}/{filename}', cfg.layers, 11000, 0)
