import cfg
import dev
import gds
import pbs
import tip
import y4x4
import numpy as np


def tbend(x, y, xsign, ysign, length):
  dq = ysign * (45 + 45 * (1 - xsign))
  x1, y1 = dev.bends(x, y, 45, 0, xsign, ysign)
  if length > 0: x1, y1 = dev.tilts(x1, y1, length, cfg.wg, dq)
  x2, y2 = dev.bends(x1, y1, 45, 45, xsign, ysign)
  return x2, y2


def chip(x, y, xsize):
  dy = 2400
  ch = cfg.ch * 0.5
  ty = cfg.ch * np.sqrt(2)

  x1, y1 = dev.sline(x + cfg.ltip, y + ch, 1000)
  x1, y2 = dev.sline(x + cfg.ltip, y - ch, 1000)

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

  print(f'ICR; {int(x11 - x1)} {int(x13 - x)}')

  return x + xsize, y


def chips(x, y):
  ysize = 3500

  chip(x, y, cfg.size)

  dev.sline(x, y + ysize, cfg.size)
  dev.sline(x, y - ysize, cfg.size)

  pbs.chip(x, y + ysize + 1300, cfg.size)
  cfg.l4x4 = 578
  y4x4.chip(x, y + ysize + 625, cfg.size, cfg.ch)
  dev.texts(x + 4600, y + ysize + 625 - 150, 'TE', 1, 'cc')
  cfg.l4x4 = 584
  y4x4.chip(x, y - ysize - 625, cfg.size, cfg.ch)
  dev.texts(x + 4600, y - ysize - 625 - 150, 'TM', 1, 'cc')
  pbs.chip(x, y - ysize - 1300, cfg.size)


if __name__ == '__main__':
  chips(0, cfg.size * 0.5)
  dev.filled(0, 0)
  gds.saveas('icr')
  gds.dlayers('icr', 'rect', 'edge')
