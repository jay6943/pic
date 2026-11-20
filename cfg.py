import os
import dat

ref = dat.jload('cfg')
ver = ref['version']
path = f'{ref['path']}-{ver}'
if not os.path.isdir(path): os.mkdir(path)
if not os.path.isdir(dat.libs): os.mkdir(dat.libs)
draft = 'draft'

wg = ref['waveguide width']
eg = ref['waveguide etched width']
ch = ref['channel spacing']
dr = ref['delay radius step']
radius = ref['radius']
angle = ['tilted angle']

w1x2 = ref['1x2']['width']
l1x2 = ref['1x2']['length']
s1x2 = ref['1x2']['spacing']
w2x2 = ref['2x2']['width']
l2x2 = ref['2x2']['length']
s2x2 = ref['2x2']['spacing']
w4x4 = ref['4x4']['width']
l4x4 = ref['4x4']['length']
s4x4 = ref['4x4']['spacing']
lpbs = ref['PBS']['length']
wpbs = ref['PBS']['wider']
rpbs = ref['PBS']['refer']
spbs = ref['PBS']['spacing']
ltpr = ref['taper']['length']
wtpr = ref['taper']['width']
ltip = ref['tip']['length']
wtip = ref['tip']['width']
lext = ref['tip']['end tip length']
lpad = ref['pad']['length']
wpad = ref['pad']['width']
sdcr = ref['directional coupler spacing']
stap = ref['tap spacing']
rings = [139, 140, 141]

duty = 0.5
period = 1.0

lchip = 10000.0
lsize = 10000.0
wkey = 400.0
wbar = 250.0
tkey = wkey + wbar
lkey = lsize + wkey
lbar = lsize + wkey + wbar
skey = lsize + wkey + wbar * 2.0
area = [[0, 0], [-1, 0], [0, 0], [-1, -1], [0, -1]]

labels = {
  'core': 1,
  'edge': 2,
  'keys': 3,
  'bars': 4,
  'cross': 5,
  'metal': 6,
  'hole': 7,
  'rect': 8,
  'text': 9
}
