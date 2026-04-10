import cfg
import dev
import gds
import elr
import pbs
import voa
import tip
import y4x4
import numpy as np


def tap(x, y, dy):
  df = elr.curve(cfg.wg, cfg.radius, 90)
  x1, y1 = dev.bends(x, y, 90, 0, 1, -1)
  dev.bends(x, y, 90, 0, -1, -1)
  dev.tline(x1, y1, df.dy - dy)


def tbend(x, y, xsign, ysign, length):
  dq = ysign * (45 + 45 * (1 - xsign))
  x1, y1 = dev.bends(x, y, 45, 0, xsign, ysign)
  if length > 0: x1, y1 = dev.tilts(x1, y1, length, cfg.wg, dq)
  x2, y2 = dev.bends(x1, y1, 45, 45, xsign, ysign)
  return x2, y2


def voa_180(x, y):
  af = elr.curve(cfg.wg, cfg.radius, 90)
  bf = elr.curve(cfg.wg, cfg.radius, 180)

  dy = (bf.dy - af.dy) * 2

  x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
  x2, y2 = dev.tline(x1, y1, dy)
  x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
  x4, y4 = voa.device(x3, y3)
  x5, y5 = dev.bends(x4, y4, 180, 0, 1, -1)
  x6, y6 = dev.sline(x5, y5, x3 - x5 + 100)
  x7, y7 = dev.bends(x6, y6, 180, 0, -1, -1)
  return x7, y


def voa_90(x, y):
  df = elr.curve(cfg.wg, cfg.radius, 90)
  x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
  x2, y2 = dev.tline(x1, y1, 2600)
  x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
  x3, y3 = dev.sline(x3, y3, 100)
  x4, y4 = voa.device(x3, y3)
  x4, y4 = dev.sline(x4, y4, 100)
  x5, y5 = dev.bends(x4, y4, 90, 0, 1, -1)
  x5, y5 = dev.tline(x5, y5, -150)
  x6, y6 = dev.bends(x5, y5, 90, 90, 1, -1)
  x7, y7 = dev.sline(x6, y6, x3 - x4 + 100)
  x8, y8 = dev.bends(x7, y7, 90, 0, -1, -1)
  x8, y8 = dev.tline(x8, y8, y - y8 + df.dy)
  x9, y9 = dev.bends(x8, y8, 90, 270, 1, 1)
  return x9, y


def chip(x, y, xsize, ysize):
  dy = 2400
  ch = cfg.ch * 0.5
  ty = cfg.ch * np.sqrt(2)

  x1, y1 = voa_90(x + cfg.ltip, y + ch)
  x1, y2 = dev.sline(x + cfg.ltip, y - ch, x1 - x - cfg.ltip)
  tap(x + 800, y2 - cfg.sdci, ysize)

  x3, y31, y32 = pbs.device('core', x1, y1)
  x3, y33, y34 = pbs.device('core', x1, y2)

  x41, y41 = tbend(x3, y31, 1,  1, 0)
  x42, y42 = tbend(x3, y32, 1, -1, ty)
  x43, y43 = tbend(x3, y33, 1,  1, ty)
  x44, y44 = tbend(x3, y34, 1, -1, 0)

  d1 = y43 - y33
  d3 = y41 - y31
  t1 = dy + ch - y31 + y - d1 - d3
  t3 = dy + ch - y31 + y - d1 - d3

  x5, y51 = tbend(x41 + d1, y41 + t1 + d1, -1, -1, ty)
  x5, y52 = tbend(x43 + d3, y43 + t1 + d3, -1, -1, 0)
  x5, y53 = tbend(x42 + d3, y42 - t3 - d3, -1,  1, 0)
  x5, y54 = tbend(x44 + d1, y44 - t3 - d1, -1,  1, ty)

  dev.tline(x41, y41, y51 - y41)
  dev.tline(x42, y42, y53 - y42)
  dev.tline(x43, y43, y52 - y43)
  dev.tline(x44, y44, y54 - y44)

  x6 = x5 + d1

  cfg.l4x4 = 578
  x11, y11 = y4x4.device(x6, y + dy, cfg.ch)
  dev.texts(x6 + 400, y11 - 150, f'TE{cfg.l4x4}', 1, 'lc')
  cfg.l4x4 = 584
  x12, y12 = y4x4.device(x6, y - dy, cfg.ch)
  dev.texts(x6 + 400, y12 - 150, f'TM{cfg.l4x4}', 1, 'lc')

  tip.device(x + cfg.ltip, y1, x)
  tip.device(x + cfg.ltip, y2, x)
  for i in [-3, -1, 1, 3]:
    x13, _ = tip.device(x11, y11 + i * ch, x + xsize)
    x13, _ = tip.device(x12, y12 + i * ch, x + xsize)

  print(f'RX; {int(x11 - x1)} {int(x13 - x)}')

  return x + xsize, y


def chips(x, y):
  ysize = 3500

  chip(x, y, cfg.size, ysize)

  dev.sline(x, y + ysize, cfg.size)
  dev.sline(x, y - ysize, cfg.size)

  pbs.chip(x, y + ysize + 1300, cfg.size)
  cfg.l4x4 = 578
  y4x4.chip(x, y + ysize + 625, cfg.size, cfg.ch)
  dev.texts(x + 4500, y + ysize + 625 - 150, 'TE', 1, 'lc')
  cfg.l4x4 = 584
  y4x4.chip(x, y - ysize - 625, cfg.size, cfg.ch)
  dev.texts(x + 4500, y - ysize - 625 - 150, 'TM', 1, 'lc')
  pbs.chip(x, y - ysize - 1300, cfg.size)


if __name__ == '__main__':
  chips(0, cfg.size * 0.5)
  dev.filled(0, 0)
  gds.saveas('rx')
  gds.dlayers('rx', 'rect', 'edge')
