import cfg
import pya


def saveas(filename):
  print('Save a GDS layer')
  layout = pya.Layout()
  layout.dbu = 0.001
  top = layout.create_cell('TOP')

  for i, points in enumerate(cfg.points):
    label = cfg.label[cfg.layers[i]]
    layer = layout.layer(pya.LayerInfo(label, 0))

    points = [pya.DPoint(x, y) for x, y in points]
    polygon = pya.DPolygon(points)
    top.shapes(layer).insert(polygon)

  print(f'writing {filename}.gds ...')
  layout.write(f'{cfg.work}/{filename}.gds')
  print()


def savelayer(filename):
  print('Save a GDS layer')
  layout = pya.Layout()
  layout.dbu = 0.001
  top = layout.create_cell('TOP')
  layer = layout.layer(pya.LayerInfo(1, 0))

  for points in cfg.points:
    points = [pya.DPoint(x, y) for x, y in points]
    polygon = pya.DPolygon(points)
    top.shapes(layer).insert(polygon)

  print(f'writing {filename}.gds ...')
  layout.write(f'{cfg.work}/{filename}.gds')
  print()


def dxf2gds(filename):
  print('DXF to GDS')
  layout = pya.Layout()
  layout.dbu = 0.001
  options = pya.LoadLayoutOptions()

  print(f'reading {filename}.dxf ...')
  layout.read(f'{cfg.work}/{filename}.dxf', options)

  print(f'writing {filename}.gds ...')
  layout.write(f'{cfg.work}/{filename}.gds')
  print()


def dlayers(filename, label1, label2):
  print(f'Difference layers, #{label1} - #{label2}')
  layout = pya.Layout()
  layout.dbu = 0.001
  print(f'reading {filename} ...')
  layout.read(f'{cfg.work}/{filename}.gds')

  top = layout.top_cell()

  layer1 = layout.find_layer(cfg.label[label1], 0)
  layer2 = layout.find_layer(cfg.label[label2], 0)

  region1 = pya.Region(top.shapes(layer1))
  region2 = pya.Region(top.shapes(layer2))

  top.shapes(layer1).clear()
  top.shapes(layer2).clear()
  top.shapes(layer2).insert(region1 - region2)

  print(f'writing {filename} ...')
  layout.write(f'{cfg.work}/{filename}.gds')
  print()


def dfiles(fp1, nlayer1, fp2, nlayer2):
  print(f'Difference, #{nlayer1} of {fp1} - #{nlayer2} of {fp2}')
  layout1 = pya.Layout()
  layout2 = pya.Layout()

  layout1.dbu = 0.001
  layout2.dbu = 0.001

  print(f'reading {fp1} ...')
  layout1.read(f'{cfg.work}/{fp1}.gds')
  print(f'reading {fp2} ...')
  layout2.read(f'{cfg.work}/{fp2}.gds')

  layer1 = layout1.find_layer(nlayer1, 0)
  layer2 = layout2.find_layer(nlayer2, 0)

  top1 = layout1.top_cell()
  top2 = layout2.top_cell()

  region1 = pya.Region(top1.shapes(layer1))
  region2 = pya.Region(top2.shapes(layer2))

  top1.shapes(layer1).clear()
  top1.shapes(layer1).insert(region1 - region2)

  print(f'writing {fp1} ...')
  layout1.write(f'{cfg.work}/{fp1}.gds')
  print()


def mfiles(fp1, nlayer1, fp2, nlayer2):
  print(f'Merge, #{nlayer1} of {fp1} - #{nlayer2} of {fp2}')
  layout1 = pya.Layout()
  layout2 = pya.Layout()

  layout1.dbu = 0.001
  layout2.dbu = 0.001

  print(f'reading {fp1} ...')
  layout1.read(f'{cfg.work}/{fp1}.gds')
  print(f'reading {fp2} ...')
  layout2.read(f'{cfg.work}/{fp2}.gds')

  layer1 = layout1.find_layer(nlayer1, 0)
  layer2 = layout2.find_layer(nlayer2, 0)

  top1 = layout1.top_cell()
  top2 = layout2.top_cell()

  region1 = pya.Region(top1.shapes(layer1))
  region2 = pya.Region(top2.shapes(layer2))

  top1.shapes(layer1).clear()
  top2.shapes(layer2).clear()
  top1.shapes(layer1).insert(region1 + region2)

  print(f'writing {fp1} ...')
  layout1.write(f'{cfg.work}/{fp1}.gds')
  print()


def texts(filename):
  print('Save a GDS layer')
  layout = pya.Layout()
  layout.dbu = 0.001

  print(f'reading {filename} ...')
  layout.read(f'{cfg.work}/{filename}.gds')
  top = layout.top_cell()
  layer = layout.layer(pya.LayerInfo(cfg.label['text'], 0))

  x, y = 11000, 0
  for title in reversed(list(cfg.label.keys())):
    text = f'{cfg.label[title]}. {title}'
    top.shapes(layer).insert(pya.DText(text, pya.DVector(x, y)))
    y += 1000

  print(f'writing {filename}.gds ...')
  layout.write(f'{cfg.work}/{filename}.gds')
  print()
