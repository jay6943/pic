import cfg
import dat
import dxf
import dev
import tip
import elr


def device(x, y):
  df = elr.curve(cfg.wg, cfg.radius, 5, cfg.draft)
  dy = 25 - cfg.spbs * 0.5
  x1, y1 = dxf.sbend('core', df, x, y, -dy)
  x2, y2 = dxf.srect('core', x1, y1, cfg.lpbs, cfg.wg)
  x5, y5 = dxf.sbend('core', df, x2, y2, dy)

  x2, y2 = dxf.srect('core', x1, y1 - cfg.spbs, cfg.lpbs, cfg.wg)
  dxf.bends('core', df, x1, y2, 0, -1, -1)
  x3, y3 = dxf.sbend('core', df, x2, y2, -dy)
  x4, y4 = dxf.srect('core', x3, y3, cfg.lpbs, cfg.wg)
  x6, y6 = dxf.srect('core', x3, y3 - cfg.spbs, cfg.lpbs, cfg.wg)
  dxf.bends('core', df, x3, y6, 0, -1, -1)
  dxf.bends('core', df, x4, y4, 0, 1, 1)
  df = elr.curve(cfg.wg, cfg.radius, 9, cfg.draft)
  # x7, y7 = dxf.sbend('core', df, x6, y6, -dy * 2)
  x7, y7 = dxf.sbend('core', df, x6, y6, y - y6 - cfg.ch)
  dxf.srect('core', x5, y5, x7 - x5, cfg.wg)
  dxf.crect('edge', x, y + cfg.eg * 0.5, x7, y7 - cfg.eg * 0.5)

  return x7, y5, y7


def polarizer(x, y, sign):
  radius = cfg.radius
  cfg.radius, angle = 100, 45
  idev = len(dat.points)
  x1, y1 = x, y
  for _ in range(10):
    x2, y2 = dev.sbend(x1, y1, angle,  sign * cfg.ch)
    x1, y1 = dev.sbend(x2, y2, angle, -sign * cfg.ch)
  x3, x4 = dxf.center(idev, x, x1, cfg.lchip)
  tip.sline(x3, y, x, '100R')
  tip.sline(x4, y, x + cfg.lchip, 'Polarizer')
  cfg.radius = radius
  return x, y + cfg.ch


def chip(x, y):
  idev = len(dat.points)
  x1, _, _ = device(x, y)
  x2, x3 = dxf.center(idev, x, x1, cfg.lchip)
  title = f'PBS-{cfg.spbs:.1f}'
  tip.sline(x2, y, x, title)
  tip.sline(x3, y, x + cfg.lchip, title)
  tip.sline(x3, y - cfg.ch, x + cfg.lchip, '')
  print(title)
  return x + cfg.lchip, y


def chips(x, y, start, stop, step):
  spbs = cfg.spbs
  for cfg.spbs in dxf.ranges(start, stop, step):
    _, y = chip(x, y + cfg.ch * 2)
  cfg.spbs = spbs
  return x + cfg.lchip, y


if __name__ == '__main__':
  chips(0, 0, 2.1, 3.1, 0.1)
  dev.saveas(f'PBC_{cfg.draft}')
