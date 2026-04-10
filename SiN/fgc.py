import os
import cfg
import dxf
import dev
import gds
import numpy as np


class coupler:
  def __init__(self):
    self.wg = cfg.wg - cfg.dw
    title = f'{self.wg * 1000:.0f}_{cfg.period * 1000:.0f}'
    self.f1 = f'{cfg.libs}/coupler_{title}_waveguide.npy'
    self.f2 = f'{cfg.libs}/coupler_{title}_grating.npy'
    if not os.path.isfile(self.f1): self.load()
    self.guide = np.load(self.f1)
    self.rects = np.load(self.f2)

  def load(self):
    x, y = 0, (cfg.wg - cfg.dw) * 0.5
    upper, lower = [[x, y]], [[x, -y]]
    arg = np.arange(0.5, 0.03, -0.001) * np.pi

    for i in range(arg.size - 1):
      a = np.tan(arg[i] * 0.5)
      b = np.tan(arg[i + 1])
      x = float((a * x - y) / (a - b))
      y = float(b * x)
      h = y + cfg.dw * 0.5
      upper += [[x, h]]
      lower += [[x, -h]]

    np.save(self.f1, upper + lower[::-1])

    df = []
    a2 = np.tan(np.arctan(y / x) * 0.5)
    x2, y2 = x, y
    for i in range(1, 31):
      x1 = float(x2 + cfg.period * (1 - cfg.duty))
      y1 = float(a2 * (x1 - x2) + y2)
      a1 = np.tan(np.arctan(y1 / x1) * 0.5)
      x2 = float(x1 + cfg.period * cfg.duty)
      y2 = float(a1 * (x2 - x1) + y1)
      a2 = np.tan(np.arctan(y2 / x2) * 0.5)
      h1 = y1 + cfg.dw * 0.5
      h2 = y2 + cfg.dw * 0.5
      df.append([[x1, h1], [x1, -h1], [x2, -h2], [x2, h2]])

    np.save(self.f2, df)


def lines(x, y, length):
  for sign in [1, -1]:
    x1, y1 = dev.sline(x, y, sign * length)
    dev.grating(x1, y1, sign)


def bends(x, y, length):
  for sign in [1, -1]:
    x1, y1 = dev.sline(x, y, sign * length)
    x2, y2 = dev.bends(x1, y1, 180, 0, sign, 1)
    x3, y3 = dev.sline(x2, y2, -sign * 100)
    x4, y4 = dev.grating(x3, y3, -sign)
    align = 'rc' if sign > 0 else 'lc'
    dev.texts(x4, y4, f'{cfg.duty}d {cfg.period}p', 0.3, align)
    dxf.srect('edge', x4, y4, -sign * 250, cfg.eg + 100)
    print(f'Grating, duty {cfg.duty}, period {cfg.period}')


def chips(x, y):
  length = cfg.size * 0.5 - 1000
  duty, period = cfg.duty, cfg.period
  for cfg.duty in [0.3, 0.4, 0.5, 0.6, 0.7]:
    for cfg.period in [0.75, 0.8, 0.85]:
      lines(x + cfg.size * 0.5, y, length)
      bends(x + cfg.size * 0.5, y + cfg.sch, length)
      y += cfg.sch * 4
  cfg.duty, cfg.period = duty, period
  return x + cfg.size, y

if __name__ == '__main__':
  filename = 'grating'
  chips(0, 0)
  # dev.filled(0, 0)
  gds.saveas(filename)
