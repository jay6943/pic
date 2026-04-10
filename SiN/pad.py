import cfg
import dxf
import gds
import elr
import numpy as np


def line(w1, w2, dx, dy, sign):
  a = dx + sign * w1 * 0.5
  b = dy + sign * w2 * 0.5

  xp = np.log10(np.linspace(1, 10, 40)) * a
  if sign < 0: xp = xp[::-1]
  yp = np.sqrt(b * b * (1 - xp * xp / (a * a)))

  return xp, dy - yp


def wire(layer, x, y, w1, w2, dx, dy, xsign, ysign):
  radius = 100

  x1, y1 = line(w1, w2, dx, dy,  1)
  x2, y2 = line(w1, w2, dx, dy, -1)

  if layer in ['metal']:
    t = (np.linspace(0, 320, 33) - 70) * np.pi / 180
  else:
    t = (np.linspace(0, 320, 33) - 74) * np.pi / 180
    x1, y1 = x1[:-5], y1[:-5]
    x2, y2 = x2[7:], y2[7:]

  r = 0 if layer in ['metal'] else cfg.eg

  x3 = (radius + r) * np.cos(t) + dx
  y3 = (radius + r) * np.sin(t) + dy + radius

  x1, y1 = x + xsign * x1, y + ysign * y1
  x2, y2 = x + xsign * x2, y + ysign * y2
  x3, y3 = x + xsign * x3, y + ysign * y3

  xp = x1.tolist() + x3.tolist() + x2.tolist()
  yp = y1.tolist() + y3.tolist() + y2.tolist()

  dxf.appends(layer, np.array([xp, yp]).transpose())

  return x + dx, y + dy


def electrode(layer, x, y, length, width, sign):
  dx, dy = 200, 100
  w = 50 if layer in ['metal'] else 50 + cfg.eg
  wire(layer, x, y, w, width, dx, dy, -1, sign)
  dxf.srect(layer, x, y, length, width)
  wire(layer, x + length, y, w, width, dx, dy, 1, sign)


def sbend(x, y, ch):
  circle, radius, angle = 100, 200, 90
  gold = elr.curve(cfg.wpad, radius, angle)
  edge = elr.curve(cfg.eg, radius, angle)

  x1, __ = dxf.srect('metal', x, y, cfg.lpad, cfg.wpad)

  m = 36
  x2, y2 = dxf.sbend('metal', gold, x1, y, ch)
  __, __ = dxf.sbend('edge', edge, x1, y, ch)
  dxf.circle('metal', x2, y2, circle, m)
  dxf.circle('edge', x2, y2, circle + cfg.eg * 0.5, m)

  idev = len(cfg.points)
  x2, y2 = dxf.sbend('metal', gold, x, y, ch)
  __, __ = dxf.sbend('edge', edge, x, y, ch)
  x3, y3 = dxf.xreverse(idev, x, y, x2, y2)
  dxf.circle('metal', x3, y3, circle, m)
  dxf.circle('edge', x3, y3, circle + cfg.eg * 0.5, m)


def bends(x, y, sign):
  circle, radius, angle = 100, 500, 30
  gold = elr.curve(cfg.wpad, radius, angle)
  edge = elr.curve(cfg.eg, radius, angle)

  x1, __ = dxf.srect('metal', x, y, cfg.lpad, cfg.wpad)

  m = 36
  x2, y2 = dxf.bends('metal', gold, x1, y, 0, 1, sign)
  __, __ = dxf.bends('edge', edge, x1, y, 0, 1, sign)
  dxf.circle('metal', x2, y2, circle, m)
  dxf.circle('edge', x2, y2, circle + cfg.eg * 0.5, m)

  x2, y2 = dxf.bends('metal', gold, x, y, 0, -1, sign)
  __, __ = dxf.bends('edge', edge, x, y, 0, -1, sign)
  dxf.circle('metal', x2, y2, circle, m)
  dxf.circle('edge', x2, y2, circle + cfg.eg * 0.5, m)


if __name__ == '__main__':
  electrode('metal', 0, 0, 400, 6, 1)
  electrode('edge', 0, 0, 400, cfg.eg, 1)
  gds.saveas('pad')
