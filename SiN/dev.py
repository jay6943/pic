import cfg
import dxf
import elr
import fgc


def srect(x, y, length, width):
  dxf.srect('edge', x, y, length, cfg.eg)
  return dxf.srect('core', x, y, length, width)


def sline(x, y, length):
  dxf.srect('edge', x, y, length, cfg.eg)
  return dxf.srect('core', x, y, length, cfg.wg)


def tline(x, y, length):
  dxf.trect('edge', x, y, length, cfg.eg)
  return dxf.trect('core', x, y, length, cfg.wg)


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


def grating(x, y, sign):
  df = fgc.coupler()
  dxf.grating('core', x, y, df, sign)
  x1, y1 = dxf.taper('edge', x, y, 150 * sign, cfg.eg, cfg.eg + 100)
  return x1, y1


def filled(x, y):
  dxf.crect('rect', x, y, x + cfg.size, y + cfg.size)


def texts(x, y, title, scale, align):
  xs = {'r': -1, 'l': 1, 'c':1}
  ys = {'t': -50, 'b': 50, 'c':0}
  xsign = xs[align[0]]
  ysign = ys[align[1]]
  d = 10 * scale * 2  # 10 when scale = 0.5
  dx, dy = dxf.texts('core', x + xsign * d, y, title, scale, align)
  x = x - dx * 0.5 if 'c' in align[0] else x
  dxf.srect('edge', x, y + ysign * scale, xsign * (dx + d * 2), dy + 10)
