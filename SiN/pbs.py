import cfg
import dxf
import dev
import gds
import cir
import tip


def arm(layer, x, y, sign):
  angle, dy, ltaper = 2, 1, 10
  wg = 1.2 + cfg.dw if sign > 0 else cfg.wpbs

  x1, y1 = dxf.taper(layer, x, y, cfg.ltpr, cfg.wtpr, cfg.wg)
  x2, y2 = dxf.sline(layer, x1, y1, 10)
  x3, y2 = dxf.taper(layer, x2, y2, ltaper, cfg.wg, wg)
  x3, y2 = dxf.srect(layer, x3, y2, cfg.lpbs, wg)
  x4, y2 = dxf.taper(layer, x3, y2, ltaper, wg, cfg.wg)
  x5, y1 = dxf.sline(layer, x4, y2, 10)
  x6, y1 = dxf.taper(layer, x5, y1, cfg.ltpr, cfg.wg, cfg.wtpr)

  return x6, y


def tail(layer, x, y, rotate, port, sign):
  df = cir.curve(cfg.wg, 5, 90)
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


def device(layer, x, y):
  ch = cfg.sch * 0.5

  x3, y31, y32 = mzi(layer, x, y + cfg.s2x2, -1, 0)
  x4, y41 = dev.sbend(x3, y31, 20,  ch)
  x4, y42 = dev.sbend(x3, y32, 20, -ch)
  x5, _, y51 = mzi(layer, x4, y41 - cfg.s2x2, 1,  1)
  x5, y52, _ = mzi(layer, x4, y42 - cfg.s2x2, 1, -1)

  return x5, y51, y52


def chip(x, y, lchip):
  idev = len(cfg.points)
  x1, _, _ = device('core', x, y)
  x5, x6 = dxf.center(idev, x, x1, lchip)

  title = f'PBS-{cfg.lpbs}'
  tip.texts(x5, y, x, title)
  tip.texts(x6, y + cfg.sch * 0.5, x + lchip, title)
  tip.device(x6, y - cfg.sch * 0.5, x + lchip)
  print(title)

  return x + lchip, y


def chips(x, y):
  y += cfg.sch * 1.5
  lpbs = cfg.lpbs
  for cfg.lpbs in dxf.arange(44, 67, 1):
    _, y = chip(x, y, cfg.size)
    y += cfg.sch * 2
  cfg.lpbs = lpbs

  return x + cfg.size, y - cfg.sch * 0.5


if __name__ == '__main__':
  filename = 'pbs'
  chips(0, 0)
  dev.filled(0, 0)
  # dxf.saveas(filename)
  gds.saveas(filename)
