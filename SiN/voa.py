import cfg
import dev
import gds
import tip
import pad
import y1x2
import y2x2


def arm(x, y, sign):
  x1, y = dev.srect(x, y, cfg.lpad, cfg.wg)
  pad.bends(x, y, sign)

  return x1, y


def device(x, y):
  angle, ch = 30, cfg.ch * 0.5

  x2, y1, y2 = y1x2.device(x, y, 1)
  x3, y3 = dev.sbend(x2, y1, angle, ch - cfg.s1x2)
  x3, y4 = dev.sbend(x2, y2, angle, cfg.s1x2 - ch)
  x5, y3 = arm(x3, y3,  1)
  x5, y4 = arm(x3, y4, -1)
  x6, y1 = dev.sbend(x5, y3, angle, cfg.s1x2 - ch)
  x6, y2 = dev.sbend(x5, y4, angle, ch - cfg.s1x2)
  x7, y1, y2 = y1x2.device(x6, y, -1)

  return x7, y


def device2x2(x, y):
  angle, ch = 30, cfg.ch * 0.5

  x1, _ = dev.sbend(x, y - ch, angle, ch - cfg.s2x2)
  x1, _ = dev.sbend(x, y + ch, angle, cfg.s2x2 - ch)
  x2, y1, y2 = y2x2.device(x1, y)
  x3, y3 = dev.sbend(x2, y1, angle, ch - cfg.s2x2)
  x3, y4 = dev.sbend(x2, y2, angle, cfg.s2x2 - ch)
  x5, y3 = arm(x3, y3,  1)
  x5, y4 = arm(x3, y4, -1)
  x6, y1 = dev.sbend(x5, y3, angle, cfg.s2x2 - ch)
  x6, y2 = dev.sbend(x5, y4, angle, ch - cfg.s2x2)
  x7, y1, y2 = y2x2.device(x6, y)
  x8, _ = dev.sbend(x7, y1, angle, ch - cfg.s2x2)
  x8, _ = dev.sbend(x7, y2, angle, cfg.s2x2 - ch)

  return x8, y


def chip(x, y, dx, lchip):
  x1 = x + dx
  x2, _ = device(x1, y)
  title = f'VOA-{cfg.lpad}-{cfg.wpad}'
  tip.texts(x1, y, x, title)
  tip.texts(x2, y, x + lchip, title)
  dev.texts((x2 + x1) * 0.5, y, title, 0.4, 'cct')
  print(f'VOA {title}')

  return x + lchip, y


def chip2x2(x, y, dx, lchip):
  x1, ch = x + dx, cfg.ch * 0.5
  x2, _ = device2x2(x1, y)
  title = f'VOA-{cfg.lpad}-{cfg.wpad}'
  tip.device(x1, y + ch, x)
  tip.device(x1, y - ch, x)
  tip.device(x2, y + ch, x + lchip)
  tip.device(x2, y - ch, x + lchip)
  dev.texts(x + cfg.ltip, y, title, 0.3, 'rc')
  dev.texts(x + lchip - cfg.ltip, y, title, 0.3, 'lc')
  dev.texts((x2 + x1) * 0.5, y, title, 0.4, 'cct')
  print(f'VOA {title}')

  return x + lchip, y


def chips(x, y):
  lpad = cfg.lpad
  for cfg.lpad in [200, 400, 600]:
    _, y = chip(x, y + cfg.ch * 2, cfg.lpad * 10, cfg.size)
  cfg.lpad = lpad

  return x + cfg.size, y + cfg.ch * 2


if __name__ == '__main__':
  chips(0, 0)
  dev.filled(0, 0)
  gds.saveas('voa')
