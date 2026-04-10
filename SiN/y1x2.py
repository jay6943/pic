import cfg
import ref
import dxf
import gds
import elr
import tip


def device(x, y, sign):
  y1 = y + cfg.s1x2
  y2 = y - cfg.s1x2
  
  if sign > 0:
    x2, _ = dxf.taper('core', x, y, cfg.ltpr, cfg.wg, cfg.wtpr)
    x3, _ = dxf.srect('core', x2, y, cfg.l1x2, cfg.w1x2)
    x5, _ = dxf.taper('core', x3, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
    x5, _ = dxf.taper('core', x3, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
  else:
    x2, _ = dxf.taper('core', x, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
    x2, _ = dxf.taper('core', x, y2, cfg.ltpr, cfg.wg, cfg.wtpr)
    x3, _ = dxf.srect('core', x2, y, cfg.l1x2, cfg.w1x2)
    x5, _ = dxf.taper('core', x3, y, cfg.ltpr, cfg.wtpr, cfg.wg)

  dxf.srect('edge', x, y, x5 - x, cfg.eg)

  return x5, y1, y2


def chip(x, y, lchip):
  x9, angle, dy = x, 5, 5
  core = elr.curve(cfg.wg, cfg.radius, angle, cfg.draft)

  idev = len(ref.points)
  for i in range(10):
    x1, y1, y2 = device(x9, y, 1)
    x2, y1 = dxf.sbend('core', core, x1, y1, dy)
    x2, y2 = dxf.sbend('core', core, x1, y2, -dy)
    x3, y1 = dxf.sbend('core', core, x2, y1, -dy)
    x3, y2 = dxf.sbend('core', core, x2, y2, dy)
    x9, y1, y2 = device(x3, y, -1)
    if i < 9: x9, _ = dxf.srect('core', x9, y, 100, cfg.wg)
  dxf.srect('edge', x, y, x9 - x, cfg.eg)
  x5, x6 = dxf.center(idev, x, x9, lchip)

  title = f'1x2-{cfg.l1x2:.1f}'
  tip.texts(x5, y, x, title)
  tip.texts(x6, y, x + lchip, title)
  print(f'{title}; {x6 - x5:.0f}')

  return x + lchip, y


def chips(x, y):
  y += cfg.sch
  l1x2 = cfg.l1x2
  for cfg.l1x2 in dxf.arange(17, 20, 0.5):
    _, y = chip(x, y, cfg.size)
    y += cfg.sch
  cfg.l1x2 = l1x2

  return x + cfg.size, y


if __name__ == '__main__':
  chips(0, 0)
  gds.saveas('1x2')
