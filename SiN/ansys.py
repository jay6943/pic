import cfg
import dxf
import gds
import elr
import fgc


def bends(path):
  wg, angle = cfg.wg - cfg.dw, 6
  df = elr.curve(wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', 0, 0, 10, wg)
  x2, y2 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.tilts('core', x2, y2, 10, wg, angle)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{angle:.0f}deg')


def sbend(path):
  wg = cfg.wg - cfg.dw
  angle = 25
  dy = 50
  dl = 10
  length = 250

  df = elr.curve(wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', -dl, 0, dl, wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, dy)
  dxf.srect('core', x2, y2, length - x2, wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{dy:.0f}h')


def ubend(path):
  wg, length = cfg.wg - cfg.dw, 20
  df = elr.curve(wg, cfg.radius, 180)
  x1, y1 = dxf.srect('core', 0, 0, length, wg)
  x1, y1 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.srect('core', x1, y1, -length, wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_180a')


def dc(path):
  wg = cfg.wg - cfg.dw
  df = elr.curve(wg, cfg.radius, 30)
  dxf.bends('core', df, 0, 0, 0, -1, -1)
  dxf.bends('core', df, 0, 0, 0, 1, -1)
  gds.savelayer(f'{path}/dc{cfg.radius:.0f}r')


def pbs(sign):
  wg = cfg.wg - cfg.dw
  cfg.radius = 500
  angle = 1
  dy = 2 * sign
  lpbs = 395
  spacing = 2.4
  ds = sign * (spacing + wg)

  df = elr.curve(wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', 0, dy + ds * 0.5, 10, wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, -dy)
  x3, y3 = dxf.srect('core', x2, y2, lpbs, wg)
  x4, y4 = dxf.sbend('core', df, x3, y3, dy)
  x5, y5 = dxf.srect('core', x4, y4, lpbs, wg)
  x6, y6 = dxf.srect('core', x4, y4 + ds, lpbs, wg)
  x7, y7 = dxf.sbend('core', df, x5, y5, -dy)
  x8, y8 = dxf.sbend('core', df, x6, y6, dy)
  dxf.srect('core', x7, y7, 10, wg)
  dxf.srect('core', x8, y8, 10, wg)
  dxf.sbend('core', df, x3, y4 + ds + dy, -dy)


def double_pbs(path):
  pbs(1)
  pbs(-1)
  gds.savelayer(f'{path}/double_pbs')


def half_pbs(path):
  wg = cfg.wg - cfg.dw
  cfg.radius = 500
  angle = 1
  lpbs = 395
  spacing = 2.4

  df = elr.curve(wg, cfg.radius, angle)

  sign = -1
  dy = sign * 2
  ds = sign * (spacing + wg)
  x2, y2 = dxf.sbend('core', df, 10, dy + ds * 0.5, -dy)
  x3, y3 = dxf.srect('core', x2, y2, lpbs, wg)
  x4, y4 = dxf.sbend('core', df, x3, y3, dy)
  x5, y5 = dxf.srect('core', x4, y4, lpbs, wg)
  x6, y6 = dxf.srect('core', x4, y4 + ds, lpbs, wg)
  x7, y7 = dxf.sbend('core', df, x5, y5, -dy)
  x8, y8 = dxf.sbend('core', df, x6, y6, dy)
  dxf.srect('core', x7, y7, 10, wg)
  dxf.srect('core', x8, y8, 10, wg)
  dxf.sbend('core', df, x3, y4 + ds + dy, -dy)

  sign = 1
  dy = sign * 2
  ds = sign * (spacing + wg)
  x1, y1 = dxf.srect('core', 0, dy + ds * 0.5, 10, wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, -dy)
  x3, y3 = dxf.srect('core', x2, y2, lpbs, wg)
  x4, y4 = dxf.sbend('core', df, x3, y3, dy)
  x5, y5 = dxf.srect('core', x4, y4, lpbs, wg)
  x7, y7 = dxf.sbend('core', df, x5, y5, dy)
  dxf.srect('core', x7, y7, 10, wg)

  gds.savelayer(f'{path}/half_pbs')


def grating_coupler(path):
  coupler = fgc.coupler()
  dxf.grating('core', 0, 0, coupler, 1)
  dxf.sline('core', -10, 0, 10)
  gds.savelayer(f'{path}/grating_gds')


if __name__ == '__main__':
  cfg.draft = 'mask'
  # bends(f'{cfg.lumerical}/euler')
  # ubend(f'{cfg.lumerical}/euler')
  # sbend(f'{cfg.lumerical}/euler')
  # double_pbs(f'{cfg.lumerical}/euler')
  # half_pbs(f'{cfg.lumerical}/euler')
  # grating_coupler(cfg.path)
  dc(f'{cfg.lumerical}')
