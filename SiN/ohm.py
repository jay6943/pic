import cfg
import dxf
import dev
import gds
import tip


def device(x, y, radius):
  l = 220
  r = cfg.radius
  cfg.radius = radius
  for _ in range(10):
    x1, y1 = dev.sline(x, y, l)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1, 1)
    x3, y3 = dev.sline(x2, y2, -50)
    x4, y4 = dev.bends(x3, y3, 180, 180, 1, -1)
    x5, y5 = dev.sline(x4, y4, l * 2)
    x6, y6 = dev.bends(x5, y5, 180, 0, 1, -1)
    x7, y7 = dev.sline(x6, y6, -50)
    x8, y8 = dev.bends(x7, y7, 180, 180, 1, 1)
    x, y = dev.sline(x8, y8, l)
  cfg.radius = r

  return x, y


def chip(x, y, lchip, radius):
  idev = len(cfg.points)
  x2, y2 = device(x, y, radius)
  x5, x6 = dxf.center(idev, x, x2, lchip)

  title = f'{radius}R'
  tip.texts(x5, y, x, title)
  tip.texts(x6, y2, x + lchip, title)
  print(f'{title}, {x5 - x:.0f}')

  return x + lchip, y


def chips(x, y):
  _, y = chip(x, y + cfg.sch, cfg.size, 50)
  _, y = chip(x, y + cfg.sch * 2, cfg.size, 75)
  _, y = chip(x, y + cfg.sch * 3, cfg.size, 100)
  _, y = chip(x, y + cfg.sch * 4, cfg.size, 125)
  return x + cfg.size, y + cfg.sch * 4


if __name__ == '__main__':
  chips(0, 0)
  gds.saveas('ohm')
