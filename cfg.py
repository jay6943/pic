import os
import ezdxf

# ver = '2.6'
# path = f'../../mask/SiN-{ver}'
# libs = f'{path}/libs'
# work = f'{path}/mask'
# if not os.path.isdir(path): os.mkdir(path)
# if not os.path.isdir(libs): os.mkdir(libs)
# if not os.path.isdir(work): os.mkdir(work)
# lumerical = '../../ansys'

doc = ezdxf.new()
msp = doc.modelspace()

layers = []
points = []
