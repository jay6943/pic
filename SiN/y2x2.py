import cfg
import dxf
import dev
import gds
import tip
import elr


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


def chip(x, y, lchip):
  ch, angle, dy = cfg.sch * 0.25, 5, 5
  df = elr.curve(cfg.wg, cfg.radius, angle)

  dh = ch * 2 - cfg.s2x2

  y1 = y + ch * 2
  y2 = y - ch * 2
  
  idev = len(cfg.points)
  x1, y3 = dev.sbend(x, y1, 15, -dh)
  x1, y4 = dev.sbend(x, y2, 15,  dh)
  for i in range(1):
    x1, y3, y4 = device(x1, y)
    if (i > 1) and (i < 9):
      x2, y3 = dxf.sbend('core', df, x1, y3, dy)
      x2, y4 = dxf.sbend('core', df, x1, y4, -dy)
      x1, y3 = dxf.sbend('core', df, x2, y3, -dy)
      x1, y4 = dxf.sbend('core', df, x2, y4, dy)
      dxf.srect('edge', x1, y, (x2 - x1) * 2, cfg.eg)
  x3, y1 = dev.sbend(x1, y3, 15,  dh)
  x3, y2 = dev.sbend(x1, y4, 15, -dh)
  x5, x6 = dxf.center(idev, x, x3, lchip)

  title = f'2x2-{cfg.l2x2:.1f}'
  tip.texts(x5, y1, x, title)
  tip.device(x5, y2, x)
  tip.texts(x6, y1, x + lchip, title)
  tip.device(x6, y2, x + lchip)
  print(f'{title}, {x6 - x5:.0f}')

  return x + lchip, y


def chips(x, y):
  y += cfg.sch * 1.5
  var = cfg.l2x2
  for cfg.l2x2 in [51.5, 52.5, 53.5, 54.5]:
    _, y = chip(x, y, cfg.size)
    y += cfg.sch * 2
  cfg.l2x2 = var

  return x + cfg.size, y - cfg.sch * 0.5

if __name__ == '__main__':
  chips(0, 0)
  gds.saveas('2x2')
