import ref
import txt
import numpy as np


def appends(layer, points):
  if layer not in ref.layers:
    ref.doc.layers.add(name=layer)
  ref.layers.append(layer)
  ref.points.append(points)


def saveas(filename):
  for i, points in enumerate(ref.points):
    ref.msp.add_lwpolyline(
      points,
      close=True,
      dxfattribs={'layer': ref.layers[i]}
    )
  ref.doc.saveas(f'{filename}.dxf')


def savelayer(filename, layers):
  for i, points in enumerate(ref.points):
    if ref.layers[i] in layers:
      ref.msp.add_lwpolyline(
        points,
        close=True,
        dxfattribs={'layer': ref.layers[i]}
      )
  ref.doc.saveas(f'{filename}.dxf')


def split(layer, dx, dy):
  for i, points in enumerate(ref.points):
    if ref.layers[i] in [layer]:
      ref.points[i] = np.array(points) + [dx, dy]


def rmatrix(angle):
  arg = angle * np.pi / 180
  rcos = np.cos(arg)
  rsin = np.sin(arg)
  return np.array([[rcos, -rsin], [rsin, rcos]])


def rotator(xp, yp, angle):
  [xp, yp] = rmatrix(angle) @ np.array([xp, yp])
  return xp, yp


def move(idev, x1, y1, x2, y2, dx, dy, angle):
  xp, yp = [], []
  p1, p2 = [], []
  for i in range(idev, len(ref.points)):
    df = np.array(ref.points[i]).transpose()
    p1 = np.array([[x1], [y1]])
    p2 = np.array([[x2], [y2]])
    if abs(angle) > 0:
      rf = rmatrix(angle)
      df = rf @ df
      p1 = rf @ p1
      p2 = rf @ p2
    xp = x1 - p1[0, 0] + dx
    yp = y1 - p1[1, 0] + dy
    ref.points[i] = df.transpose() + [xp, yp]
  return p2[0, 0] + xp, p2[1, 0] + yp


def rotation(idev, x, y, xt, yt, angle):
  tf, px, py = [], [], []
  for i in range(idev, len(ref.points)):
    rf = rmatrix(angle)
    df = rf @ np.array(ref.points[i]).transpose()
    sf = rf @ [[x], [y]]
    tf = rf @ [[xt], [yt]]
    px = x - sf[0][0]
    py = y - sf[1][0]
    ref.points[i] = df.transpose() + [px, py]
  return tf[0][0] + px, tf[1][0] + py


def xreverse(idev, x, y, xt, yt):
  for i in range(idev, len(ref.points)):
    df = np.array(ref.points[i]) - [x, y]
    ref.points[i] = df * [-1, 1] + [x, y]
  return x * 2 - xt, yt


def xrevshift(idev, x, y, xt, yt):
  for i in range(idev, len(ref.points)):
    df = np.array(ref.points[i]) - [x, y]
    ref.points[i] = df * [-1, 1] + [xt, y * 2 - yt]
  return xt, y * 2 - yt


def yreverse(idev, x, y, xt, yt):
  for i in range(idev, len(ref.points)):
    df = np.array(ref.points[i]) - [x, y]
    ref.points[i] = df * [1, -1] + [x, y]
  return xt, y * 2 - yt


def center(idev, x1, x2, lchip):
  ldev = x2 - x1
  x3, _ = move(idev, x1, 0, x2, 0, (lchip - ldev) * 0.5, 0, 0)
  return x3 - ldev, x3


def arange(xstart, xstop, xstep):
  var = np.arange(xstart, xstop + xstep * 0.5, xstep)
  var = np.round(var, 3)
  return var


def circle(layer, x, y, radius, n):
  t = np.linspace(0, np.pi * 2, n)
  xp = x + radius * np.cos(t)
  yp = y + radius * np.sin(t)
  appends(layer, np.array([xp, yp]).transpose())
  return x, y


def arc(layer, x, y, radius, start, stop, n):
  t = np.linspace(start, stop, n) * np.pi / 180
  xp = x + radius * np.cos(t)
  yp = y + radius * np.sin(t)
  xp = np.append(xp, np.array([x]))
  yp = np.append(yp, np.array([y]))
  appends(layer, np.array([xp, yp]).transpose())
  return x, y


def crect(layer, x1, y1, x2, y2):
  appends(layer, [[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
  return x2, y2


def srect(layer, x, y, length, width):
  w = width * 0.5
  points = [[x, y - w], [x + length, y - w], [x + length, y + w], [x, y + w]]
  appends(layer, points)
  return x + length, y


def trect(layer, x, y, length, width):
  w = width * 0.5
  crect(layer, x - w, y, x + w, y + length)
  return x, y + length


def taper(layer, x, y, length, start, stop):
  a, b = start * 0.5, stop * 0.5
  points = [[x, y - a], [x + length, y - b], [x + length, y + b], [x, y + a]]
  appends(layer, points)
  return x + length, y


def triangle(layer, x, y, width, height):
  points = [[x, y + height], [x + width * 0.5, y], [x - width * 0.5, y]]
  appends(layer, points)
  return x, y


def bends(layer, df, x, y, angle, xsign, ysign):
  xp, yp = df.x, df.y
  if abs(angle) > 0: xp, yp = rotator(xp, yp, angle)
  xp, yp = x + xp * xsign, y + yp * ysign
  xt = (xp[df.m-1] + xp[df.m]) * 0.5
  yt = (yp[df.m-1] + yp[df.m]) * 0.5
  appends(layer, np.array([xp, yp]).transpose())
  return xt, yt


def sbend(layer, df, x, y, dy):
  sign = 1 if dy > 0 else -1
  yo = dy - df.dy * 2 * sign
  xo = yo * sign / np.tan(df.angle / 180 * np.pi)
  x1, y1 = df.x[df.m - 1], df.y[df.m - 1] * sign
  x2, y2 = df.x[df.m], df.y[df.m] * sign
  x3, y3 = df.dx * 2 + xo - x1, dy - y1
  x4, y4 = df.dx * 2 + xo - x2, dy - y2
  points = [
    [x + x1, y + y1],
    [x + x2, y + y2],
    [x + x3, y + y3],
    [x + x4, y + y4]
  ]
  appends(layer, points)
  x1, y1 = bends(layer, df, x, y, 0, 1, sign)
  x2, y2 = x1 + df.dx + xo, y1 + df.dy * sign + yo
  x3, y3 = bends(layer, df, x2, y2, 0, -1, -sign)
  return x3 + df.dx, y3 + df.dy * sign


def tilts(layer, x, y, length, width, angle):
  w = width * 0.5
  xp, yp = [0, length, length, 0], [w, w, -w, -w]
  xp, yp = rotator(xp, yp, angle)
  xp, yp = xp + x, yp + y
  appends(layer, np.array([xp, yp]).transpose())
  return (xp[1] + xp[2]) * 0.5, (yp[1] + yp[2]) * 0.5


def texts(layer, x, y, title, scale, align):
  spacing, ht, lt = 50, 100, 0
  for ch in title:
    lt += txt.xmax[ch] + 5 if ch in txt.xmax else spacing
  x -= txt.xalign[align[0]] * lt * scale
  y -= txt.yalign[align[1]] * ht * scale
  for ch in title:
    if ch in txt.xmax:
      for xy in txt.chars[ch]:
        points = []
        for xt, yt in xy:
          points.append([xt * scale + x, yt * scale + y])
        appends(layer, points)
      x += (txt.xmax[ch] + 5) * scale
    else: x += spacing * scale
  return lt * scale, ht * scale
