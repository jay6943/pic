import os
import dxf
import scipy
import numpy as np


class curve:
  def __init__(self, wg, radius, angle, draft):
    self.wg = wg
    self.r = radius
    self.angle = angle
    self.draft = draft
    self.length = 0

    df = self.load()
    self.m = df['m']
    self.x = df['x']
    self.y = df['y']
    self.l = df['l']
    self.dx = (self.x[self.m - 1] + self.x[self.m]) * 0.5
    self.dy = (self.y[self.m - 1] + self.y[self.m]) * 0.5

  def device(self, fp):
    num = self.r * 0.2 if self.draft != 'mask' else self.r * 4

    s = np.sqrt(self.angle / 180)
    c = np.sqrt(np.pi * 0.5)
    m = round(num * s)
    t = np.linspace(0, s, m)
    p = t * c

    xt, yt = scipy.special.fresnel(t)
    x = yt * c * self.r
    y = xt * c * self.r
    px = np.sin(p * p)
    py = np.cos(p * p)

    length = 0
    for i in range(m - 1):
      dx = x[i + 1] - x[i]
      dy = y[i + 1] - y[i]
      length += np.sqrt(dx * dx + dy * dy)
    length *= 2

    width = self.wg * 0.5
    xinner = x - width * px
    yinner = y + width * py
    xouter = x + width * px
    youter = y - width * py

    xf = np.hstack((xinner, xouter[::-1]))
    yf = np.hstack((yinner, youter[::-1]))

    rf = dxf.rmatrix(self.angle)
    sf = rf @ np.array([-x[-1], y[-1]]).reshape(2, 1)
    cf = rf @ np.array([-1 * xf, yf])
    cf += np.array([x[-1] - sf[0], y[-1] - sf[1]]).reshape(2, 1)

    xp = np.hstack((xf[:m], cf[0][:m][::-1]))
    yp = np.hstack((yf[:m], cf[1][:m][::-1]))
    xp = np.hstack((xp, cf[0][m:][::-1]))
    yp = np.hstack((yp, cf[1][m:][::-1]))
    xp = np.hstack((xp, xf[m:]))
    yp = np.hstack((yp, yf[m:]))

    np.save(fp, {'m': m * 2, 'x': xp, 'y': yp, 'l': length})
    print(f'-- Euler 곡선; {self.wg}W, {self.r}R', end=', ')
    print(f'{self.angle}도 회전, {m} points ({self.draft})')

  def load(self):
    w = round(self.wg, 4)
    r = round(self.r, 4)
    a = round(self.angle, 4)
    fp = f'{dxf.libs}/euler_{w}_{r}_{a}_{self.draft}.npy'
    if not os.path.isfile(fp): self.device(fp)
    return np.load(fp, allow_pickle=True).item()
