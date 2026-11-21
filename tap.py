import cfg
import dat
import dxf
import dev
import tip


def device(x, y):
  y -= cfg.stap
  dev.bends(x, y, cfg.angle, 0, -1, -1)
  x1, y1 = dev.sbend(x, y, cfg.angle, cfg.stap - cfg.ch)
  return x1, y1


def chip(x, y):
  idev = len(dat.points)
  x1, _ = device(x, y)
  x2, _ = dev.sline(x, y, x1 - x)
  x3, x4 = dxf.center(idev, x, x2, cfg.lchip)

  title = f'TAP-{cfg.stap:.1f}'
  tip.sline(x3, y, x, title)
  tip.sline(x4, y, x + cfg.lchip, title)
  tip.sline(x4, y - cfg.ch, x + cfg.lchip, '')
  print(title)

  return x + cfg.lchip, y


def chips(x, y, start, stop, step):
  stap = cfg.stap
  for cfg.stap in dxf.ranges(start, stop, step):
    _, y = chip(x, y + cfg.ch * 2)
  cfg.stap = stap
  return x, y + cfg.ch


if __name__ == '__main__':
  chips(0, 0, 1.3, 2.1, 0.1)
  dev.savedxf(f'tap_{cfg.draft}')
