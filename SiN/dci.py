import cfg
import dxf
import dev
import gds
import tip
import numpy as np


def device(x, y, angle):
  y -= cfg.sdci
  dev.bends(x, y, angle, 0, -1, -1)
  x1, y1 = dev.sbend(x, y, angle, cfg.sdci - cfg.sch)
  return x1, y1


def chip(x, y, lchip):
  idev = len(cfg.points)
  x1, y1 = device(x, y, 30)
  x2, y2 = dev.sline(x, y, x1 - x)
  x3, x4 = dxf.center(idev, x, x2, lchip)

  title = f'DC-{cfg.sdci:.1f}'
  tip.texts(x3, y, x, title)
  tip.texts(x4, y, x + lchip, title)
  tip.device(x4, y - cfg.sch, x + lchip)
  print(title)

  return x, y


def chips(x, y):
  sdci = cfg.sdci
  for cfg.sdci in np.linspace(1.5, 2.6, 12):
    _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.sdci = sdci
  return x, y


if __name__ == '__main__':
  filename = 'direction_coupler'
  chips(0, 0)
  gds.saveas(filename)
