import cfg
import dxf
import dev


def device(x, y, sign):
  w = [cfg.wg, cfg.wtip]
  l = [cfg.ltip - cfg.lext, cfg.lext]

  x1, _ = dxf.taper('core', x, y, sign * l[0], w[0], w[1])
  x2, _ = dxf.srect('core', x1, y, sign * l[1], w[1])
  dxf.srect('edge', x, y, x2 - x, cfg.eg)
  
  return x2, y


def sline(x, y, xend, title):
  if xend > x: sign, align = 1, 'lc'
  else: sign, align = -1, 'rc'
  if sign * (xend - x) > cfg.ltip:
    x1, _ = dev.sline(x, y, xend - x - sign * cfg.ltip)
  else: x1 = x
  x2, _ = device(x1, y, sign)
  if title:
    dev.texts(x2 - sign * cfg.ltip, y - cfg.ch * 0.5, title, 0.3, align)
  return x2, y


def refer(x, y):
  ch = cfg.ch * 0.5
  title = 'ref'
  chip(x, y, cfg.lchip)
  dev.texts(x + cfg.ltip, y - ch, title, 0.3, 'rc')
  dev.texts(x + cfg.lchip - cfg.ltip, y - ch, title, 0.3, 'lc')
  return x, y


def chip(x, y, lchip):
  x1 = x + cfg.ltip
  x2, _ = dev.sline(x1, y, lchip - 2 * cfg.ltip)
  device(x1, y, -1)
  device(x2, y,  1)
  return x + lchip, y


def chips(x, y, ranges):
  y += cfg.ch
  wtip = cfg.wtip
  for cfg.wtip in ranges:
    chip(x, y, cfg.lchip)
    title = f'TIP-{cfg.wtip:.2f}'
    dev.texts(x + cfg.ltip, y - cfg.ch * 0.5, title, 0.3, 'rc')
    dev.texts(x + cfg.lchip - cfg.ltip, y - cfg.ch * 0.5, title, 0.3, 'lc')
    y += cfg.ch
  cfg.wtip = wtip
  return x + cfg.lchip, y


if __name__ == '__main__':
  chips(0, 0, dxf.arange(0.34, 0.54, 0.02))
  dev.saveas('tip')
