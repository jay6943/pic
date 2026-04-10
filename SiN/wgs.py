import cfg
import dxf
import dev
import gds
import tip


def device(x, y, turns):
  zlength = 8000

  x1, y1 = dev.srect(x, y, zlength, cfg.wg)
  for _ in range(turns):
    x2, y2 = dev.bends(x1, y1, 180, 0, 1, 1)
    x3, y3 = dev.srect(x2, y2, -zlength, cfg.wg)
    x4, y4 = dev.bends(x3, y3, 180, 0, -1, 1)
    x1, y1 = dev.srect(x4, y4, zlength, cfg.wg)
  x6, y6 = dev.srect(x1, y1, 100, cfg.wg)
  x7, y7 = dev.bends(x6, y6, 90, 0, 1, -1)
  ylength = y6 - y - (y6 - y7) * 2
  x8, y8 = dev.tilts(x7, y7, ylength, cfg.wg, -90)
  x, y = dev.bends(x8, y8, 90, 270, 1, 1)

  return x, y


def chip(x, y, lchip, turns):
  idev = len(cfg.points)
  x2, y2 = device(x, y, turns)
  x5, x6 = dxf.center(idev, x, x2, lchip)

  title = f'l{turns}'
  tip.texts(x5, y, x, title)
  tip.texts(x6, y2, x + lchip, title)
  print(f'{title}; 길이 {x6 - x5:.0f} um, 칩 크기 {x2 - x:.0f} um')

  return x + lchip, y


def chips(x, y):
  _, y = chip(x, y + cfg.sch, cfg.size, 1)
  _, y = chip(x, y + cfg.sch * 5, cfg.size, 2)
  _, y = chip(x, y + cfg.sch * 8, cfg.size, 3)
  return x + cfg.size, y + cfg.sch * 8


if __name__ == '__main__':
  chips(0, 0)
  gds.saveas('waveguide_loss')
