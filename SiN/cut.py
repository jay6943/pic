import cfg
import dxf
import gds
import key
import numpy as np


def wafer():
  radius = 150 * 0.5 * 1000
  radian = np.linspace(-70, 250, 81) * np.pi / 180
  
  x = radius * np.cos(radian)
  y = radius * np.sin(radian)

  dxf.appends('edge', np.array([x, y]).transpose())

  t = 4000
  r = radius + 5000

  dxf.crect('core', -r, -r, t - r, t - r)
  dxf.crect('core', -r,  r, t - r, r - t)
  dxf.crect('core',  r, -r, r - t, t - r)
  dxf.crect('core',  r,  r, r - t, r - t)


def cells(x, y, size, n, title):
  cs = cfg.size * 0.5
  dy = cs + cfg.wkey

  for i in range(n):
    dx = size * (i - n * 0.5) + 200
    key.bars(x + dx - cfg.wkey, y)
    dxf.srect('rect', x + dx, y + dy, cfg.size, cfg.size)
    dxf.texts('text', x + dx + cs, y + cs, title, 25, 'cc')


def tooling(x, y, size, rmax):
  for i in range(11):
    j = i % 4 + 1
    n = 10 if i % 10 else 8
    dx = size * (i - 5)
    dy = dx - size * 0.5

    if j != 4: cells(x, y + dy, size, n, f'{j}:02d')
    else: key.frame(x + cfg.wkey, y + dy + cfg.wkey, 2)
    
    dxf.srect('keys', x + dx, y, 10, rmax * 2)
  
  dxf.srect('keys', x - rmax, y + size * 6, rmax * 2, 10)
  dxf.srect('keys', x - rmax, y + size * 2, rmax * 2, 10)
  dxf.srect('keys', x - rmax, y - size * 2, rmax * 2, 10)
  dxf.srect('keys', x - rmax, y - size * 6, rmax * 2, 10)

  wafer()
  gds.saveas('wafer')


def cell_position_1x4():
  labels = ['01', '02', '03', '04'] * 2
  labels.insert(4, '00')
  labels = [labels[:] for _ in range(9)]
  nx, ny = len(labels[0]), len(labels)

  size = cfg.wkey + cfg.size
  for j in range(ny):
    y = size * (j - (ny - 1) * 0.5)
    for i in range(nx):
      x = size * (i - nx * 0.5)
      dxf.srect('rect', x, y, size, size)
      dxf.texts('text', x + size * 0.5, y, labels[i][j], 25, 'cc')

  wafer()
  gds.saveas('mapping')


def cell_position_3x1():
  labels = [f'{i:02d}' for i in [1, 2, 3]] * 3
  for i, label in enumerate(labels):
    if '1' in label: labels[i] = f'{label}-04'
  labels = [labels[:] for _ in range(9)]
  nx, ny = len(labels[0]), len(labels)

  size = cfg.wkey + cfg.size
  for j in range(ny):
    y = size * (j - (ny - 1) * 0.5)
    for i in range(nx):
      x = size * (i - nx * 0.5)
      dxf.srect('rect', x, y, size, size)
      dxf.texts('text', x + size * 0.5, y, labels[i][j], 25, 'cc')

  wafer()
  gds.saveas('mapping')


if __name__ == '__main__': cell_position_3x1()
