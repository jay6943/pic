import os
import cfg
import dxf
import dev
import tip
import numpy as np


def device(fp):
  l = 0.02 if cfg.draft != 'draft' else 0.1
  x = 0
  y = cfg.wg * 0.5
  a = np.pi * 0.5

  upper = [[x,  y]]
  lower = [[x, -y]]
  for i in range(int(round(100 / l, 3))):
    x = x + l
    y = y + np.tan(0.5 * a) * l
    a = np.arctan(y / x)
    upper += [[x,  y]]
    lower += [[x, -y]]
  df = np.array(upper + lower[::-1])

  rects = []
  l = cfg.period * (1 - cfg.duty)
  for _ in range(30):
    x1 = x + l
    y1 = y + np.tan(0.5 * a) * l
    x = x + cfg.period
    y = y + np.tan(0.5 * a) * cfg.period
    a = np.arctan(y / x)
    x2 = x
    y2 = y
    xy = np.array([[x1, y1], [x1, -y1], [x2, -y2], [x2, y2]])
    rects.append(xy)

  np.save(fp, {'guide': df, 'grating': rects})


def grating(layer, x, y, sign):
  w = round(cfg.wg, 3)
  d = round(cfg.duty * 100, 3)
  p = round(cfg.period, 3)
  fp = f'{cfg.libs}/coupler_{w}_{p}_{d:.0f}.npy'
  if not os.path.isfile(fp): device(fp)
  df = np.load(fp, allow_pickle=True).item()
  dxf.appends(layer, df['guide'] * [sign, 1] + [x, y])
  for xy in df['grating']: dxf.appends(layer, xy * [sign, 1] + [x, y])


def chip(x, y, sign):
  grating('core', x, y, sign)
  x1, y1 = dxf.taper('edge', x, y, 150 * sign, cfg.eg, 100)
  return x1, y1


def chips(x, y, start, stop, step):
  duty = cfg.duty
  period = cfg.period
  for cfg.duty in dxf.ranges(start, stop, step):
    y += cfg.ch
    tip.chip(x, y)
    for cfg.period in dxf.ranges(1.0, 1.6, 0.1):
      title = f'{cfg.period}-{cfg.duty*100:.0f}'
      x1, y1 = x + cfg.lchip - cfg.ltip, y + cfg.ch
      tip.sline(x1, y1, x, '')
      x2, y2 = chip(x1, y1, 1)
      dev.texts(x2 + 10, y2, title, 0.4, 'lc')
      # dx = cfg.lchip * 0.5
      # for sign in [1, -1]:
      #   x1, y1 = dev.sline(x + dx, y + cfg.ch * 2, sign * (dx - cfg.ltip))
      #   x2, y2 = chip(x1, y1, sign)
      #   align = 'lc' if sign > 0 else 'rc'
      #   dev.texts(x2 + sign * 10, y2, title, 0.4, align)
      # y += cfg.ch * 2
      y += cfg.ch
      print(f'Grating period = {cfg.period} um')
  cfg.period = period
  cfg.duty = duty
  return x + cfg.lchip, y + cfg.ch * 2


if __name__ == '__main__':
  chips(0, 0, 0.48, 0.52, 0.01)
  dev.saveas('grating')
