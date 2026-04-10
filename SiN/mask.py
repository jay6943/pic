import cfg
import adb.dxf as dxf
import adb.gds as gds
import dev
import key
import pbs
import dly
import voa
import dci
import fgc
import tip
import sem
import y2x2


def delays(x, y):
  key.frame(x, y, 1)
  dev.filled(x, y)
  _, y1 = tip.chip(x, y + cfg.sch, cfg.size)
  _, y1 = voa.chips(x, y1)
  _, y1 = tip.chip(x, y1, cfg.size)
  _, y1 = dly.chips(x, y1 + cfg.sch * 5)
  _, y1 = tip.chip(x, y1 + cfg.sch * 30, cfg.size)
  _, y1 = tip.chip(x, y1 + cfg.sch * 31, cfg.size)
  _, y1 = voa.chip2x2(x, y1 + cfg.sch * 5, 4000, cfg.size)
  _, y1 = y2x2.chip(x, y1 + cfg.sch * 6, cfg.size)
  sem.chips(x, y + cfg.sch * 33)
  sem.chips(x, y + cfg.sch * 64)


def pbses(x, y):
  key.frame(x, y, 1)
  dev.filled(x, y)
  _, y1 = tip.chip(x, y + cfg.sch, cfg.size)
  _, y1 = pbs.chips(x, y1)
  _, y1 = tip.chip(x, y1, cfg.size)
  _, y1 = pbs.chips(x, y1)
  _, y1 = tip.chip(x, y1, cfg.size)


def couplers(x, y):
  key.frame(x, y, 1)
  dev.filled(x, y)
  _, y1 = tip.chip(x, y + cfg.sch, cfg.size)
  _, y1 = tip.chips(x, y1)
  _, y1 = tip.chip(x, y1, cfg.size)
  _, y1 = dci.chips(x, y1)
  _, y1 = tip.chip(x, y1 + cfg.sch, cfg.size)
  _, y1 = fgc.chips(x, y1 + cfg.sch)


def filled(x, y):
  key.frame(x, y, 2)
  dxf.split('metal', cfg.skey, -cfg.skey)


def chips(region):
  xt = cfg.wbar + cfg.wkey
  yt = cfg.wbar + cfg.wkey
  if 0 in region: key.cross(0, 0)
  if 1 in region: delays(xt - cfg.skey, yt)
  if 2 in region: pbses(xt, yt)
  if 3 in region: couplers(xt - cfg.skey, yt - cfg.skey)
  if 4 in region: filled(xt, yt - cfg.skey)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3, 4])
  # dxf.saveas(filename)
  gds.saveas(filename)
  gds.dlayers(filename, 'rect', 'edge')
  gds.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: gds.texts(filename)
