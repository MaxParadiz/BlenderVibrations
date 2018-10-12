import bpy
import numpy as np

def getNAtoms( lines ):
 for line in lines:
  if 'NAtoms=' in line:
   return int(line.split()[1])

def getFreqStart( lines ):
 for i,elem in enumerate(lines):
  if 'Frequencies' in elem:
   return i

def buildMatrix( lines, start, NAtoms ):
 NModes = NAtoms*3-6
 FreqMatrix = []
 frequencies = []
 step = start
 for block in range(0,NAtoms-2):
  s = start+block*(NAtoms+7)
  col1 = []
  col2 = []
  col3 = []
  frequencies.append(list(map(float,lines[s].split()[2:5])))
  s += 4
  for atom in range(0,NAtoms):
   s += 1
   h = lines[s].split()
   col1.append(list(map(float,h[2:5])))
   col2.append(list(map(float,h[5:8])))
   col3.append(list(map(float,h[8:11])))
  FreqMatrix.append(col1)
  FreqMatrix.append(col2)
  FreqMatrix.append(col3)
 return np.asarray(frequencies).flatten(), np.asarray(FreqMatrix)

def load_matrix(filename):
 lines = open(filename,'r').read().split('\n')
 NAtoms = getNAtoms(lines)
 print(NAtoms)
 FreqStart = getFreqStart( lines )
 print(FreqStart)
 return buildMatrix(lines,FreqStart,NAtoms)





def load_coordinates(filename):
 lines = open(filename,'r').read().split('\n')
 NAtoms = getNAtoms(lines)
 atoms = []
 coords = []
 for i,elem in enumerate(lines):
  if 'Input orientation' in elem:
   index = i
 for i in lines[index+5:index+5+NAtoms]:
  h = i.split()
  atoms.append(h[1])
  coords.append(list(map(float,h[3:6])))
 return atoms,np.asarray(coords)

file = '/home/max/Desktop/LoadCoords/RFreqAnharmonic.log'

frequencies, FreqMatrix = load_matrix(file)
atoms,coords = load_coordinates(file)

atom_properties = {'1':{'scale':0.5,'name':'H','Color':(0.85,0.85,0.85,1)}
         ,'5':{'scale':0.8,'name':'B','Color':(234.0/255,178.0/255,58.0/255,1)}
         ,'6':{'scale':0.71,'name':'C','Color':(0.20,0.20,0.20,1)}
         ,'7':{'scale':0.65,'name':'N','Color':(82.0/255,140.0/255,230.0/255,1)}
         ,'8':{'scale':0.63,'name':'O','Color':(245.0/255,62.0/255,79.0/255,1)}
         ,'9':{'scale':0.61,'name':'F','Color':(60.0/255,224.0/255,120.0/255,1)}}

#Make the Materials
for atom_type in atom_properties:
 New_material = bpy.data.materials.new(atom_properties[atom_type]['name'])
 New_material.use_nodes = True
 New_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = atom_properties[atom_type]['Color']

#Loat the atoms
D = bpy.data
for i in range(0,len(atoms)):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(coords[i]),size=atom_properties[atoms[i]]['scale']*1.5)
 bpy.context.scene.objects[i].data.materials.append(D.materials[atom_properties[atoms[i]]['name']])

scn = bpy.context.scene
scn.frame_start = 1
scn.frame_end = 200

def Vibrate( modes,speed=1,amp = 1,phase=[] ):
 phase = np.concatenate([phase,np.zeros(len(modes)-len(phase))])
 for t in range(0,200):
  scn.frame_set(t)
  displace = 0
  p = 0
  for mode in modes:
   displace += amp*np.sin(2*speed*frequencies[mode]/300*np.pi*t/200+phase[p])*FreqMatrix[mode]
   p += 1
  tcoords = displace+coords
  for i in range(0,len(coords)):
   obj = scn.objects[i]
   obj.location=tcoords[i]
   obj.keyframe_insert(data_path='location')
  
 


