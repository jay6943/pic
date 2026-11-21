import dat
import dxf
import cfg
import dev
import tip


def device(x, y, radius):
  length = 220
  r = cfg.radius
  cfg.radius = radius
  for _ in range(10):
    x1, y1 = dev.sline(x, y, length)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1, 1)
    x3, y3 = dev.sline(x2, y2, -50)
    x4, y4 = dev.bends(x3, y3, 180, 180, 1, -1)
    x5, y5 = dev.sline(x4, y4, length * 2)
    x6, y6 = dev.bends(x5, y5, 180, 0, 1, -1)
    x7, y7 = dev.sline(x6, y6, -50)
    x8, y8 = dev.bends(x7, y7, 180, 180, 1, 1)
    x, y = dev.sline(x8, y8, length)
  cfg.radius = r

  return x, y


def chip(x, y, radius):
  idev = len(dat.points)
  x2, y2 = device(x, y, radius)
  x5, x6 = dxf.center(idev, x, x2, cfg.lchip)

  title = f'{radius}R'
  tip.sline(x5, y, x, title)
  tip.sline(x6, y2, x + cfg.lchip, title)
  print(f'{title}, {x5 - x:.0f}')

  return x + cfg.lchip, y


def chips(x, y):
  _, y = chip(x, y + cfg.ch, 50)
  _, y = chip(x, y + cfg.ch * 2, 75)
  _, y = chip(x, y + cfg.ch * 3, 100)
  _, y = chip(x, y + cfg.ch * 4, 125)
  return x + cfg.lchip, y + cfg.ch * 4


if __name__ == '__main__':
  chips(0, 0)
  dev.saveas(f'ohm_{cfg.draft}')
