import cfg
import fontTools.ttLib as ftl
import fontTools.pens.basePen as ftp

class PrintPen(ftp.BasePen):
  def __init__(self, glyphSet):
    super().__init__(glyphSet)
    self.coordinates = []

  def _moveTo(self, p0):
    self.coordinates.append(('move', p0))

  def _lineTo(self, p1):
    self.coordinates.append(('line', p1))

  def _curveToOne(self, p1, p2, p3):
    self.coordinates.append(('curve', p1, p2, p3))

  def _closePath(self):
    self.coordinates.append(('close',))

def print_glyph_outline(ttf_path, char, layer, x, y):
  font = ftl.TTFont(ttf_path)
  cmap = font.getBestCmap()
  glyph_set = font.getGlyphSet()
  glyph_name = cmap[ord(char)]
  glyph = glyph_set[glyph_name]
  pen = PrintPen(glyph_set)
  glyph.draw(pen)

  points, blocks, old, curves = [], [], '', False
  for item in pen.coordinates:
    ch = item
    for c in ['(', '\'', ' ', ')']:
      ch = str(ch).replace(c, '')
    ch = ch.split(',')

    if ch[0] != 'close':
      i = 1
      while i < len(ch):
        xt = round(float(ch[i]) * 6 * 0.01 + x, 4)
        yt = round(float(ch[i+1]) * 6 * 0.01 + y, 4)
        points.append((xt, yt))
        i += 2
    elif char in ['b', 'd', 'g', 'o', 'p', 'q', 'O', 'Q', '0', '8']:
      if old == 'curve':
        curves = False if curves else True
      if old != 'curve' or not curves:
        blocks.append(points)
        points = []
    else:
      blocks.append(points)
      points = []

    old = ch[0]

  print(f'\'{char}\': [', end='')
  for i, points in enumerate(blocks):
    cfg.msp.add_lwpolyline(points, close=True, dxfattribs={'layer': layer})
    if i < len(blocks) - 1: print(f'{points}, ', end='')
    else: print(f'{points}],')

  xp = []
  for i, points in enumerate(blocks):
    for x, y in points: xp.append(x)

  return max(xp)


if __name__ == '__main__':
  fontfile = '../data/Roboto/static/Roboto-Bold.ttf'

  # Roboto-Regular.ttf 파일 경로와 출력할 글자 지정
  # print_glyph_outline(fontfile, 'c', 'active')

  large = [chr(i) for i in range(ord('a'), ord('z') + 1)]
  small = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
  value = [chr(i) for i in range(ord('0'), ord('9') + 1)]
  symbl = [',', '.', '-', '+', '*', '#', '&', '@', '!', '/', ':', ';']
  texts = large + small + value + symbl

  xmax, xc = [], 0
  for chars in texts:
    xc = print_glyph_outline(fontfile, chars, 'active', 0, 0)
    xmax.append(xc)

  for i, chars in enumerate(texts):
    print(f'\'{chars}\': {xmax[i]},', end=' ')

  cfg.doc.saveas(f'{cfg.path}/fonts.dxf')
