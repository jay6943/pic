import os
import ref
import numpy as np


class curve:
  def __init__(self, wg, radius, angle, draft):
    self.wg = wg
    self.r = radius
    self.angle = angle
    self.m = 10 if draft != 'mask' else 20

    df = self.load()
    self.x = df['x']
    self.y = df['y']
    self.dx = self.x[-1] * self.r
    self.dy = self.y[-1] * self.r

  def device(self, fp):
    width = self.wg * 0.5

    n = int(self.m * self.angle / 45)
    t = np.linspace(0, self.angle, n) * np.pi / 180

    x = np.cos(t)
    y = np.sin(t)

    xinner = (self.r - width) * x - self.r * x[0]
    yinner = (self.r - width) * y - self.r * y[0]
    xouter = (self.r + width) * x - self.r * x[0]
    youter = (self.r + width) * y - self.r * y[0]
    xp = np.append(xinner, xouter[::-1])
    yp = np.append(yinner, youter[::-1])

    np.save(fp, {'x': xp, 'y': yp})
    print('-- Circular;', self.r, self.angle, self.m)

  def load(self):
    w = str(round(self.wg, 4))
    r = str(round(self.r, 4))
    a = str(round(self.angle, 4))
    fp = f'{ref.libs}/cir_{w}_{r}_{a}_{self.m}.npy'
    if not os.path.isfile(fp): self.device(fp)
    return np.load(fp, allow_pickle=True).item()
