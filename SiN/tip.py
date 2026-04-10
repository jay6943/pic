import cfg
import dxf
import dev
import gds


def device(x, y, dx):
  sign = 1 if dx > x else -1
  w = [cfg.wg, cfg.wtip + cfg.dw]
  l = [cfg.ltip - cfg.lext, cfg.lext]

  if (dx - x) * sign > cfg.ltip:
    x, _ = dev.sline(x, y, dx - x - cfg.ltip * sign)
  x1, _ = dxf.taper('core', x, y, sign * l[0], w[0], w[1])
  x2, _ = dxf.srect('core', x1, y, sign * l[1], w[1])
  dxf.srect('edge', x, y, x2 - x, cfg.eg)
  return x1, y


def texts(x, y, dx, title):
  align = 'lc' if dx > x else 'rc'
  dy = cfg.sch * 0.5
  x, _ = device(x, y, dx)
  dev.texts(x, y - dy, title, 0.3, align)


def chip(x, y, lchip):
  title = f'TIP-{cfg.wtip:.2f}'
  dx = lchip * 0.5
  texts(x + dx, y, x, title)
  texts(x + dx, y, x + lchip, title)
  return x + lchip, y


def chips(x, y):
  y += cfg.sch
  wtip = cfg.wtip
  for cfg.wtip in dxf.arange(0.2, 0.4, 0.02):
    chip(x, y, cfg.size)
    y += cfg.sch
  cfg.wtip = wtip
  return x + cfg.size, y


if __name__ == '__main__':
  filename = 'tip'
  chips(0, 0)
  # dev.filled(0, 0)
  gds.saveas(filename)
