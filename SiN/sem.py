import cfg
import dxf
import dev
import gds


def wgs(x, y, align):
  sign = 1 if 'l' in align[0] else -1
  dxf.sline('core', x, y + cfg.s2x2, sign * cfg.lext)
  x1, _ = dxf.srect('edge', x, y, sign * cfg.lext, cfg.eg)
  dev.texts(x1, y, 'WG', 0.3, align)


def pbses(x, y, align):
  sign = 1 if 'l' in align[0] else -1
  dxf.srect('core', x, y + cfg.s2x2, sign * cfg.lext, 1.2 + cfg.dw)
  dxf.srect('core', x, y - cfg.s2x2, sign * cfg.lext, 1.85 + cfg.dw)
  x1, _ = dxf.srect('edge', x, y, sign * cfg.lext, cfg.eg)
  dev.texts(x1, y, 'PBS', 0.3, align)


def couplers(x, y, align):
  sign = 1 if 'l' in align[0] else -1
  dxf.sline('core', x, y, sign * cfg.lext)
  dxf.sline('core', x, y + cfg.sdci, sign * cfg.lext)
  x1, _ = dxf.srect('edge', x, y, sign * cfg.lext, cfg.eg)
  dev.texts(x1, y, 'DC', 0.3, align)


def tips(x, y, align):
  sign = 1 if 'l' in align[0] else -1
  for w in [0.2, 0.3, 0.4]:
    title = f'TIP {w}'
    dxf.srect('core', x, y, sign * cfg.lext, w + cfg.dw)
    x1, _ = dxf.srect('edge', x, y, sign * cfg.lext, cfg.eg)
    dev.texts(x1, y, title, 0.3, align)
    y += cfg.sch


def chips(x, y):
  for i, align in enumerate(['lc', 'rc']):
    wgs(x + cfg.size * i, y, align)
    pbses(x + cfg.size * i, y + cfg.sch, align)
    couplers(x + cfg.size * i, y + cfg.sch * 2, align)
    tips(x + cfg.size * i, y + cfg.sch * 3, align)

  return x, y + cfg.sch * 9


if __name__ == '__main__':
  chips(0, 0)
  gds.saveas('sem')
