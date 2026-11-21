import cfg
import dev
import tip
import pad
import y2x2


def arm(x, y, sign):
  x1, y = dev.srect(x, y, cfg.lpad, cfg.wg)
  pad.electrode('metal', x, y, cfg.lpad, 6, sign)
  pad.electrode('edge', x, y, cfg.lpad, cfg.eg, sign)

  return x1, y


def device(x, y):
  angle, ch = 10, cfg.ch * 0.5
  x2, y1, y2 = y2x2.device(x, y)
  x3, y3 = dev.sbend(x2, y1, angle, ch - cfg.s2x2)
  x3, y4 = dev.sbend(x2, y2, angle, cfg.s2x2 - ch)
  x5, y3 = arm(x3, y3,  1)
  x5, y4 = arm(x3, y4, -1)
  x6, y1 = dev.sbend(x5, y3, angle, cfg.s2x2 - ch)
  x6, y2 = dev.sbend(x5, y4, angle, ch - cfg.s2x2)
  x7, y1, y2 = y2x2.device(x6, y)

  return x7, y1, y2


def chip(x, y, dx, angle):
  ch = cfg.ch * 0.5

  x1 = x + dx
  y1 = y + ch
  y2 = y - ch

  x3, _ = dev.sbend(x1, y1, angle, cfg.s2x2 - ch)
  x3, _ = dev.sbend(x1, y2, angle, ch - cfg.s2x2)
  x4, y3, y4 = device(x3, y)
  x5, _ = dev.sbend(x4, y3, angle, ch - cfg.s2x2)
  x5, _ = dev.sbend(x4, y4, angle, cfg.s2x2 - ch)

  tip.sline(x1, y1, x, 'Switch')
  tip.sline(x1, y2, x, '')
  tip.sline(x5, y1, x + cfg.lchip, 'Switch')
  tip.sline(x5, y2, x + cfg.lchip, '')

  return x + cfg.lchip, y


def chips(x, y, angle):
  lpad = cfg.lpad
  for cfg.lpad in [200, 400, 600]:
    _, y = chip(x, y + cfg.ch * 2, cfg.lpad * 10, angle)
  cfg.lpad = lpad

  return x + cfg.lchip, y + cfg.ch * 2


if __name__ == '__main__':
  chip(0, 0, 4000, 20)
  # chip(0, 0, 4000, 10)
  dev.saveas(f'switch_{cfg.draft}')
