import cfg
import dat
import dxf
import dev
import tip


def polarizer(x, y, sign):
  radius = cfg.radius
  cfg.radius, angle = 50, 45
  idev = len(dat.points)
  x1, y1 = x, y
  for _ in range(20):
    x2, y2 = dev.sbend(x1, y1, angle,  sign * cfg.ch)
    x1, y1 = dev.sbend(x2, y2, angle, -sign * cfg.ch)
  x3, x4 = dxf.center(idev, x, x1, cfg.lchip)
  tip.sline(x3, y, x, '100R')
  tip.sline(x4, y, x + cfg.lchip, 'Polarizer')
  cfg.radius = radius
  return x, y + cfg.ch


def arm(layer, x, y, sign):
  ltaper = 10
  wg = 1.2 if sign > 0 else cfg.wpbs

  x1, y1 = dxf.taper(layer, x, y, cfg.ltpr, cfg.wtpr, cfg.wg)
  x2, y2 = dxf.srect(layer, x1, y1, 10, cfg.wg)
  x3, y2 = dxf.taper(layer, x2, y2, ltaper, cfg.wg, wg)
  x3, y2 = dxf.srect(layer, x3, y2, cfg.lpbs, wg)
  x4, y2 = dxf.taper(layer, x3, y2, ltaper, wg, cfg.wg)
  x5, y1 = dxf.srect(layer, x4, y2, 10, cfg.wg)
  x6, y1 = dxf.taper(layer, x5, y1, cfg.ltpr, cfg.wg, cfg.wtpr)

  return x6, y


def tail(layer, x, y, rotate, port, sign):
  df = dev.circular(cfg.wg, 5, 90)
  dxf.taper(layer, x, y, sign * cfg.ltpr, cfg.wg, cfg.wtpr)
  x1, y1 = dxf.bends(layer, df, x, y, rotate, 1, port)
  return x1, y1


def mzi(layer, x, y, inport, outport):
  y1 = y + cfg.s2x2
  y2 = y - cfg.s2x2
  y3 = y + inport * cfg.s2x2

  x1, _ = dxf.taper(layer, x, y3, cfg.ltpr, cfg.wg, cfg.wtpr)
  tail(layer, x1 - cfg.ltpr, y - inport * cfg.s2x2, 90, inport, 1)

  x2, _ = dxf.srect(layer, x1, y, cfg.l2x2, cfg.w2x2)
  x5, _ = arm(layer, x2, y1,  1)
  x5, _ = arm(layer, x2, y2, -1)

  x6, _ = dxf.srect(layer, x5, y, cfg.l2x2, cfg.w2x2)

  if not outport:
    dxf.taper(layer, x6, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
    dxf.taper(layer, x6, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
  elif outport < 0:
    dxf.taper(layer, x6, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
    tail(layer, x6 + cfg.ltpr, y + outport * cfg.s2x2, 270, outport, -1)
  elif outport > 0:
    dxf.taper(layer, x6, y2, cfg.ltpr, cfg.wtpr, cfg.wg)
    tail(layer, x6 + cfg.ltpr, y + outport * cfg.s2x2, 270, outport, -1)

  x7 = x6 + cfg.ltpr
  dxf.srect('edge', x, y, x7 - x, cfg.w2x2 + cfg.eg)

  return x7, y1, y2


def device(layer, x, y, ch):
  x1, y11, y12 = mzi(layer, x, y + cfg.s2x2, -1, 0)
  x2, y21 = dev.sbend(x1, y11, cfg.angle,  ch)
  x2, y22 = dev.sbend(x1, y12, cfg.angle, -ch)
  x3, _, y31 = mzi(layer, x2, y21 - cfg.s2x2, 1,  1)
  x3, y32, _ = mzi(layer, x2, y22 - cfg.s2x2, 1, -1)

  return x3, y31, y32


def chip(x, y, ch):
  idev = len(dat.points)
  x1, _, _ = device('core', x, y, ch)
  x5, x6 = dxf.center(idev, x, x1, cfg.lchip)

  title = f'PBS-{cfg.lpbs:.0f}'
  tip.sline(x5, y, x, title)
  tip.sline(x6, y + cfg.ch * 0.5, x + cfg.lchip, title)
  tip.sline(x6, y - cfg.ch * 0.5, x + cfg.lchip, '')
  print(title)

  return x + cfg.lchip, y


def chips(x, y, start, stop, step):
  y += cfg.ch * 1.5
  lpbs = cfg.lpbs
  for cfg.lpbs in dxf.ranges(start, stop, step):
    _, y = chip(x, y, cfg.ch * 0.5)
    y += cfg.ch * 2
  cfg.lpbs = lpbs

  return x + cfg.lchip, y - cfg.ch * 0.5


if __name__ == '__main__':
  chips(0, 0, 44, 66, 1)
  dev.saveas(f'PBS_{cfg.draft}')
