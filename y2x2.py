import cfg
import dat
import dxf
import dev
import tip


def device(x, y):
  y1 = y + cfg.s2x2
  y2 = y - cfg.s2x2

  x2, _ = dxf.taper('core', x, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
  x2, _ = dxf.taper('core', x, y2, cfg.ltpr, cfg.wg, cfg.wtpr)
  x3, _ = dxf.srect('core', x2, y, cfg.l2x2, cfg.w2x2)
  x5, _ = dxf.taper('core', x3, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
  x5, _ = dxf.taper('core', x3, y2, cfg.ltpr, cfg.wtpr, cfg.wg)

  dxf.srect('edge', x, y, x5 - x, cfg.eg)

  return x5, y1, y2


def chip(x, y):
  ch = cfg.ch * 0.5
  dy = ch - cfg.s2x2

  y1 = y + ch
  y2 = y - ch
  
  idev = len(dat.points)
  x1, y3 = dev.sbend(x, y1, cfg.angle, -dy)
  x1, y4 = dev.sbend(x, y2, cfg.angle,  dy)
  x1, y3, y4 = device(x1, y)
  x3, y1 = dev.sbend(x1, y3, cfg.angle,  dy)
  x3, y2 = dev.sbend(x1, y4, cfg.angle, -dy)
  x5, x6 = dxf.center(idev, x, x3, cfg.lchip)

  title = f'2x2-{cfg.l2x2:.0f}'
  tip.sline(x5, y1, x, title)
  tip.sline(x5, y2, x, '')
  tip.sline(x6, y1, x + cfg.lchip, title)
  tip.sline(x6, y2, x + cfg.lchip, '')
  print(f'{title}, {x6 - x5:.0f}')

  return x + cfg.lchip, y


def chips(x, y, start, stop, step):
  y += cfg.ch * 1.5
  var = cfg.l2x2
  for cfg.l2x2 in dxf.ranges(start, stop, step):
    _, y = chip(x, y)
    y += cfg.ch * 2
  cfg.l2x2 = var

  return x + cfg.lchip, y - cfg.ch * 0.5

if __name__ == '__main__':
  chips(0, 0, 51.5, 54.5, 1)
  dev.saveas(f'2x2_{cfg.draft}')
