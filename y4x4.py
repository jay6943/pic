import cfg
import dat
import dxf
import dev
import tip
import numpy as np


def device(x, y, ch):
  y1 = y + ch * 0.5
  y2 = y - ch * 0.5

  x1, y3 = dev.sbend(x, y1, 30, cfg.s4x4 * 3 - ch * 0.5)
  x2, y4 = dev.sbend(x, y2, 30, ch * 0.5 - cfg.s4x4)
  dev.sline(x1, y3, x2 - x1)

  x3, _ = dxf.taper('core', x2, y3, cfg.ltpr, cfg.wg, cfg.wtpr)
  x3, _ = dxf.taper('core', x2, y4, cfg.ltpr, cfg.wg, cfg.wtpr)

  x4, _ = dxf.srect('core', x3, y, cfg.l4x4, cfg.w4x4)

  y5 = y + cfg.s4x4 * np.array([3, 1, -1, -3])
  x5, _ = dxf.taper('core', x4, y5[0], cfg.ltpr, cfg.wtpr, cfg.wg)
  x6, _ = dxf.taper('core', x4, y5[1], cfg.ltpr, cfg.wtpr, cfg.wg)
  x6, _ = dxf.taper('core', x4, y5[2], cfg.ltpr, cfg.wtpr, cfg.wg)
  x5, _ = dxf.taper('core', x4, y5[3], cfg.ltpr, cfg.wtpr, cfg.wg)
  dxf.srect('edge', x2, y, x5 - x2, cfg.eg + cfg.w4x4)

  x8, _ = dev.sline(x6, y5[1], 30)
  x8, _ = dev.sline(x6, y5[2], 30)

  if ch < cfg.ch:
    x7, y1 = dev.sbend(x5, y5[0], 45, ch * 1.5 - cfg.s4x4 * 3)
    x9, y2 = dev.sbend(x8, y5[1], 20, ch * 0.5 - cfg.s4x4)
    x9, y3 = dev.sbend(x8, y5[2], 20, cfg.s4x4 - ch * 0.5)
    x7, y4 = dev.sbend(x5, y5[3], 45, cfg.s4x4 * 3 - ch * 1.5)

    x8, _ = dev.sline(x7, y1, 100)
    x6, _ = dev.sline(x9, y2, x8 - x9)
    x9, _ = dev.sline(x9, y3, x8 - x9)
    x8, _ = dev.sline(x7, y4, 100)

    x11, y2 = dev.sbend(x6, y2, 30, -ch)
    x12, y3 = dev.sbend(x8, y3, 30, -ch)
    x13, y4 = dev.sbend(x8, y4, 60, ch * 2)
    x16, y2 = dev.sline(x11, y2, x13 - x11)
    x16, y3 = dev.sline(x12, y3, x13 - x12)
    x16, y1 = dev.sline(x7, y1, x16 - x7)
  else:
    x7, y1 = dev.sbend(x5, y5[0], 90, ch * 1.5 - cfg.s4x4 * 3)
    x9, y2 = dev.sbend(x8, y5[1], 45, ch * 0.5 - cfg.s4x4)
    x9, y3 = dev.sbend(x8, y5[2], 45, cfg.s4x4 - ch * 0.5)
    x7, y4 = dev.sbend(x5, y5[3], 90, cfg.s4x4 * 3 - ch * 1.5)

    x6, _ = dev.sline(x9, y2, 200)
    x9, _ = dev.sline(x9, y3, 10)
    x8, _ = dev.sline(x7, y1, x9 - x7)
    x8, _ = dev.sline(x7, y4, x9 - x7)

    x11, y2 = dev.sbend(x6, y2, 45, -ch)
    x12, y3 = dev.sbend(x8, y3, 45, -ch)
    x13, y4 = dev.sbend(x8, y4, 45, ch * 2)
    x16, y2 = dev.sline(x11, y2, x13 - x11)
    x16, y3 = dev.sline(x12, y3, x13 - x12)
    x16, y1 = dev.sline(x7, y1, x16 - x7)

  return x16, y


def chip(x, y, ych):
  idev = len(dat.points)
  x1, _ = device(x, y, ych)
  x2, x3 = dxf.center(idev, x, x1, cfg.lchip)

  title = f'4x4-{cfg.l4x4:.0f}'
  tip.sline(x2, y + ych * 0.5, x, '')
  tip.sline(x2, y - ych * 0.5, x, '')
  dev.texts(x + cfg.lext, y, title, 0.3, 'rc')

  for i, ich in enumerate([3, 1, -1, -3]):
    title = f'{cfg.l4x4:.0f}-{4-i:.0f}'
    x4, y4 = x + cfg.lchip - cfg.lext, y + ych * 0.5 * ich
    tip.sline(x3, y4, x + cfg.lchip, '')
    dev.texts(x4, y4 - ych * 0.5, title, 0.3, 'lc')
  print(f'4x4 MMI, {cfg.l4x4:.0f} um')

  return x + cfg.lchip, y


def chips(x, y, start, stop, step):
  ch = cfg.ch
  cfg.ch = 250
  y += cfg.ch * 1.25
  l4x4 = cfg.l4x4
  for cfg.l4x4 in dxf.ranges(start, stop, step):
    _, y = chip(x, y, cfg.ch * 0.5)
    y += cfg.ch * 2
  cfg.l4x4 = l4x4
  cfg.ch = ch

  return x + cfg.lchip, y - cfg.ch * 0.75


if __name__ == '__main__':
  chip(0, 0, 250)
  dev.saveas(f'4x4_{cfg.draft}')
