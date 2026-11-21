import cfg
import dat
import dxf
import dev
import tip


def device(x, y, sign):
  y1 = y + cfg.s1x2
  y2 = y - cfg.s1x2

  if sign > 0:
    x1, _ = dxf.taper('core', x, y, cfg.ltpr, cfg.wg, cfg.wtpr)
    x2, _ = dxf.srect('core', x1, y, cfg.l1x2, cfg.w1x2)
    x3, _ = dxf.taper('core', x2, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
    x3, _ = dxf.taper('core', x2, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
  else:
    x1, _ = dxf.taper('core', x, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
    x1, _ = dxf.taper('core', x, y2, cfg.ltpr, cfg.wg, cfg.wtpr)
    x2, _ = dxf.srect('core', x1, y, cfg.l1x2, cfg.w1x2)
    x3, _ = dxf.taper('core', x2, y, cfg.ltpr, cfg.wtpr, cfg.wg)

  dxf.srect('edge', x, y, x3 - x, cfg.eg)

  return x3, y1, y2


def chip(x, y):
  dy = cfg.ch * 0.5 - cfg.s1x2

  idev = len(dat.points)
  x1, y1, y2 = device(x, y, 1)
  x2, y1 = dev.sbend(x1, y1, cfg.angle,  dy)
  x2, y2 = dev.sbend(x1, y2, cfg.angle, -dy)
  x5, x6 = dxf.center(idev, x, x2, cfg.lchip)

  title = f'1x2-{cfg.l1x2:.1f}'
  tip.sline(x5, y, x, title)
  tip.sline(x6, y1, x + cfg.lchip, title)
  tip.sline(x6, y2, x + cfg.lchip, '')
  print(f'{title}; {x6 - x5:.0f}')

  return x + cfg.lchip, y


def chips(x, y, start, stop, step):
  y += cfg.ch * 1.5
  l1x2 = cfg.l1x2
  for cfg.l1x2 in dxf.ranges(start, stop, step):
    _, y = chip(x, y)
    y += cfg.ch * 2
  cfg.l1x2 = l1x2

  return x + cfg.lchip, y


if __name__ == '__main__':
  chips(0, 0, 16, 20, 0.5)
  dev.saveas(f'1x2_{cfg.draft}')
