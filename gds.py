import ref
import pya

options = pya.SaveLayoutOptions()
options.format = 'GDS2'
options.gds2_max_vertex_count = 4000


def saveas(filename, labels):
  layout = pya.Layout()
  layout.dbu = 0.001
  top = layout.create_cell('TOP')

  for i, points in enumerate(ref.points):
    label = labels[ref.layers[i]]
    layer = layout.layer(pya.LayerInfo(label, 0))

    points = [pya.DPoint(x, y) for x, y in points]
    polygon = pya.DPolygon(points)
    top.shapes(layer).insert(polygon)

  layout.write(f'{filename}.gds', options)


def savelayer(filename):
  layout = pya.Layout()
  layout.dbu = 0.001
  top = layout.create_cell('TOP')
  layer = layout.layer(pya.LayerInfo(1, 0))

  for points in ref.points:
    points = [pya.DPoint(x, y) for x, y in points]
    polygon = pya.DPolygon(points)
    top.shapes(layer).insert(polygon)

  layout.write(f'{filename}.gds', options)


def dxf2gds(filename):
  layout = pya.Layout()
  layout.dbu = 0.001

  layout.read(f'{filename}.dxf')
  layout.write(f'{filename}.gds', options)


def dlayers(filename, labels, label1, label2):
  layout = pya.Layout()
  layout.dbu = 0.001
  layout.read(f'{filename}.gds')

  top = layout.top_cell()

  layer1 = layout.find_layer(labels[label1], 0)
  layer2 = layout.find_layer(labels[label2], 0)

  region1 = pya.Region(top.shapes(layer1))
  region2 = pya.Region(top.shapes(layer2))

  top.shapes(layer1).clear()
  top.shapes(layer2).clear()
  top.shapes(layer2).insert(region1 - region2)

  layout.write(f'{filename}.gds', options)


def players(filename, labels, label1, label2):
  layout = pya.Layout()
  layout.dbu = 0.001
  layout.read(f'{filename}.gds')

  top = layout.top_cell()

  layer1 = layout.find_layer(labels[label1], 0)
  layer2 = layout.find_layer(labels[label2], 0)

  region1 = pya.Region(top.shapes(layer1))
  region2 = pya.Region(top.shapes(layer2))

  top.shapes(layer1).clear()
  top.shapes(layer2).clear()
  top.shapes(layer2).insert(region1 + region2)

  layout.write(f'{filename}.gds', options)


def dfiles(fp1, nlayer1, fp2, nlayer2):
  layout1 = pya.Layout()
  layout2 = pya.Layout()

  layout1.dbu = 0.001
  layout2.dbu = 0.001

  layout1.read(f'{fp1}.gds')
  layout2.read(f'{fp2}.gds')

  layer1 = layout1.find_layer(nlayer1, 0)
  layer2 = layout2.find_layer(nlayer2, 0)

  top1 = layout1.top_cell()
  top2 = layout2.top_cell()

  region1 = pya.Region(top1.shapes(layer1))
  region2 = pya.Region(top2.shapes(layer2))

  top1.shapes(layer1).clear()
  top1.shapes(layer1).insert(region1 - region2)

  layout1.write(f'{fp1}.gds', options)


def mfiles(fp1, nlayer1, fp2, nlayer2):
  layout1 = pya.Layout()
  layout2 = pya.Layout()

  layout1.dbu = 0.001
  layout2.dbu = 0.001

  layout1.read(f'{fp1}.gds')
  layout2.read(f'{fp2}.gds')

  layer1 = layout1.find_layer(nlayer1, 0)
  layer2 = layout2.find_layer(nlayer2, 0)

  top1 = layout1.top_cell()
  top2 = layout2.top_cell()

  region1 = pya.Region(top1.shapes(layer1))
  region2 = pya.Region(top2.shapes(layer2))

  top1.shapes(layer1).clear()
  top2.shapes(layer2).clear()
  top1.shapes(layer1).insert(region1 + region2)

  layout1.write(f'{fp1}.gds', options)


def texts(filename, labels, x, y):
  layout = pya.Layout()
  layout.dbu = 0.001

  layout.read(f'{filename}.gds')
  top = layout.top_cell()
  layer = layout.layer(pya.LayerInfo(labels['text'], 0))

  for title in reversed(list(labels.keys())):
    text = f'{labels[title]}. {title}'
    top.shapes(layer).insert(pya.DText(text, pya.DVector(x, y)))
    y += 1000

  layout.write(f'{filename}.gds', options)
