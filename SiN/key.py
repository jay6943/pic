import cfg
import dxf
import gds


def cross(x, y):
  points = [
    [x - cfg.lbar, y + cfg.wbar], [x - cfg.wbar, y + cfg.wbar],
    [x - cfg.wbar, y + cfg.lbar], [x + cfg.wbar, y + cfg.lbar],
    [x + cfg.wbar, y + cfg.wbar], [x + cfg.lbar, y + cfg.wbar],
    [x + cfg.lbar, y - cfg.wbar], [x + cfg.wbar, y - cfg.wbar],
    [x + cfg.wbar, y - cfg.lbar], [x - cfg.wbar, y - cfg.lbar],
    [x - cfg.wbar, y - cfg.wbar], [x - cfg.lbar, y - cfg.wbar]
  ]
  dxf.appends('cross', points)


def bars(x, y):
  points = [
    [x, y], [x, y + cfg.lkey],
    [x + cfg.wkey, y + cfg.lkey], [x + cfg.wkey, y + cfg.wkey],
    [x + cfg.lkey, y + cfg.wkey], [x + cfg.lkey, y]
  ]
  dxf.appends('hole', points)


def triangle(x, y):
  dx, dy = 30, 10
  dl = dx * 2
  ds = cfg.size - dy
  dxf.triangle('core', x + dx + dy, y + dy, dl, dl)
  dxf.triangle('core', x + dx + dy, y + ds, dl, -dl)
  dxf.triangle('core', x - dx + ds, y + dy, dl, dl)
  dxf.triangle('core', x - dx + ds, y + ds, dl, -dl)


def xrect(layer, x, y, z, w, t, m):
  for i in range(m):
    xp = x + i * t
    dxf.crect(layer, xp, y, xp + z, y + w)


def yrect(layer, x, y, z, w, t, m):
  for i in range(m):
    yp = y + i * t
    dxf.crect(layer, x, yp, x + z, yp + w)


def key1(layer, x, y, align):
  xp = x + (align - 1) * 1100
  yp = y

  for i in [488, 508, 534, 938]:
    yrect(layer, xp + i, yp + 69, 4, 4, 8, 7)

  for i in [67, 93, 113]:
    xrect(layer, xp + 583.5, yp + i, 3, 4, 6, 51)

  xrect(layer, xp + 1014, yp + 93, 4, 4, 8, 7)
  xrect(layer, xp + 1145, yp + 60, 4, 70, 8, 13)
  yrect(layer, xp + 1315, yp + 45, 70, 4, 8, 13)


def key2(layer, x, y, align):
  xp = x + 5060
  yp = y + 200
  
  dxf.crect('bars', xp, yp, xp + 340, yp + 50)

  xp += 0.25
  yp += 25

  dxf.srect(layer, xp + 302, yp, 20, 20)
  dxf.texts(layer, xp + 242, yp, '0' + str(align), 0.2, 'lc')

  l, s, t = 10, 7.5, 2.5

  for i in range(1, 7):
    w = i * 0.5
    s = s + (i - 1) * 4.5 + 20

    for j in range(0, 10, 2): dxf.srect(layer, xp + s + w * j, yp - 5, w, l)
    dxf.srect(layer, xp + s + w * 2, yp - 5 + l, w, l)
    dxf.srect(layer, xp + s + w * 7, yp - 5 + l, w, l)

    t = t + (i - 1) * 4.5 + 20

    idev = len(cfg.points)
    dxf.texts(layer, xp, yp, str(w), 0.05, 'lb')
    dxf.move(idev, xp, yp, 0, 0, t, -10, 90)


def key3(layer, x, y):
  dxf.crect('bars', x, y, x + 340, y + 100)
  dxf.srect(layer, x + 37.5, y + 65, 10, 10)

  for i in range(11):
    dxf.srect(layer, x + 15 + i * 5.2, y + 22.5, 3, 10)
    dxf.srect(layer, x + 80, y + i * 5.2 + 39, 10, 3)
  
  for i in range(21): dxf.srect(layer, x + 119 + i * 5, y + 70, 2, 40)

  dxf.srect(layer, x + 257.5, y + 65, 20, 20)

  for i in range(11):
    w = 10 if i % 5 == 0 else 8
    dxf.srect(layer, x + 240.4 + i * 5.1, y + 17.5 - w * 0.5, 3.2, w)
    dxf.srect(layer, x + 315, y + 39.5 + i * 5.1, w, 3.2)


def frame(x, y, align):
  x -= cfg.wkey
  y -= cfg.wkey

  bars(x, y)

  key1('bars', x, y, align)
  key2('keys', x, y, align)
  key3('keys', x + 7815, y + 150)

  x4, y4 = 8750, 150
  x5, y5 = 8950, 100
  x6, y6 = 9900, 150

  dxf.crect('bars', x + x4, y + y4, x + x4 + 100, y + y4 + 100)
  dxf.crect('bars', x + x5, y + y5, x + x5 + 100, y + y5 + 200)
  dxf.crect('bars', x + x6, y + y6, x + x6 + 200, y + y6 + 100)
  dxf.srect('keys', x + x6 + 50, y + y6 + 50, 10, 80)
  dxf.srect('keys', x + x6 + 100, y + y6 + 50, 5, 80)
  dxf.srect('keys', x + x6 + 150, y + y6 + 50, 1, 80)

  idev = len(cfg.points)
  key1('bars', x, y, 1)
  dxf.move(idev, x, y, 0, 0, 0, align * 1100 + 800, 270)

  idev = len(cfg.points)
  key2('keys', x, y, align)
  dxf.move(idev, x, y, 0, 0, 400, 0, 90)


def contact_align_key(layer, x, y, scale, sign):
  for i in [0, 1, 3, 4, 5]:
    x1, y1 = x + (70 + 260 * i) * scale, y + 130 * scale
    x2, y2 = x + 590 * scale, y + (690 - 260 * i) * scale

    l, w = 120 * scale, 28 * scale
    x3 = x1 if sign > 0 else x2
    y3 = y1 if sign > 0 else y2 - 40 * scale
    dxf.srect(layer, x3, y3, l, w)
    dxf.srect(layer, x3 + 46 * scale, y3, w, l)

    l, d = 40 * scale, 80 * scale
    x4 = x2 if sign > 0 else x1
    y4 = y2 if sign > 0 else y1 + 40 * scale
    dxf.srect(layer, x4, y4, l, l)
    dxf.srect(layer, x4 + d, y4, l, l)
    dxf.srect(layer, x4, y4 - d, l, l)
    dxf.srect(layer, x4 + d, y4 - d, l, l)

  return x, y


def contact_align_keys(layer, x, y, sign):
  xo = x + cfg.size * 0.5
  yo = y + cfg.size * 0.5

  for i in range(4):
    idev = len(cfg.points)
    xt, rt = xo + 1300, 1
    
    for _ in range(4):
      contact_align_key(layer, xt, yo, rt, sign)
      xt += 1820 * rt
      rt *= 0.5
    
    dxf.move(idev, xo, yo, 0, 0, 0, 0, 90 * i)
  
  dxf.srect(layer, x, yo - 1000, cfg.size, 5)

  print('Contact Align Keys')


if __name__ == '__main__':
  xw = cfg.wbar + cfg.wkey
  yw = cfg.wbar + cfg.wkey
  cross(0, 0)
  frame(xw - cfg.skey, yw, 1)
  frame(xw, yw, 1)
  frame(xw - cfg.skey, yw - cfg.skey, 2)
  frame(xw, yw - cfg.skey, 3)
  gds.saveas('key')
