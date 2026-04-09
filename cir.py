import os
import cfg
import numpy as np


class curve:
  def __init__(self, wg, radius, angle):
    self.wg = wg
    self.angle = angle
    self.radius = radius
    self.m = 10 if cfg.draft != 'mask' else 20
    self.m = 10 if self.wg > cfg.wg else self.m

    df = self.load()
    self.x = df['x']
    self.y = df['y']
    self.dx = self.x[-1] * self.radius
    self.dy = self.y[-1] * self.radius

  def device(self, fp):
    width = self.wg * 0.5

    n = int(self.m * self.angle / 45)
    t = np.linspace(0, self.angle, n) * np.pi / 180

    x = np.cos(t)
    y = np.sin(t)

    xinner = (self.radius - width) * x - self.radius * x[0]
    yinner = (self.radius - width) * y - self.radius * y[0]
    xouter = (self.radius + width) * x - self.radius * x[0]
    youter = (self.radius + width) * y - self.radius * y[0]
    xp = np.append(xinner, xouter[::-1])
    yp = np.append(yinner, youter[::-1])

    np.save(fp, {'x': xp, 'y': yp})
    print('-- Circular;', self.radius, self.angle, self.m)

  def load(self):
    w = str(round(self.wg, 4))
    r = str(round(self.radius, 4))
    a = str(round(self.angle, 4))
    fp = f'{cfg.libs}/cir_{w}_{r}_{a}_{self.m}.npy'
    if not os.path.isfile(fp): self.device(fp)
    return np.load(fp, allow_pickle=True).item()
