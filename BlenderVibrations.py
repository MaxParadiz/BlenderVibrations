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

frequencies, FreqMatrix = load_matrix('/home/max/Desktop/LoadCoords/RFreqAnharmonic.log')



def load(filename):
 f = open(filename,'r').read()
 f = f.split('\n')[2:]
 f.pop()
 atoms = []
 coords = []
 for i in f:
  h = i.split()
  atoms.append(h[0])
  coords.append(list(map(float,h[1:])))
 return atoms,np.asarray(coords)


atoms,coords = load('/home/max/Desktop/LoadCoords/R.xyz')

scale = {"H":0.5,"B":0.8,"C":0.71,"N":0.65,"O":0.63,"F":0.61}


#Loat the atoms
D = bpy.data
for i in range(0,len(atoms)):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, location=(coords[i]),size=scale[atoms[i]]*1.5)
 bpy.context.scene.objects[i].data.materials.append(D.materials[atoms[i]])

scn = bpy.context.scene
scn.frame_start = 1
scn.frame_end = 200

def Vibrate( modes ):
 for t in range(0,200):
  scn.frame_set(t)
  displace = 0
  for mode in modes:
   displace += np.sin(2*frequencies[mode]/300*np.pi*t/100)*FreqMatrix[mode]
  tcoords = displace+coords
  for i in range(0,len(coords)):
   obj = scn.objects[i]
   obj.location=tcoords[i]
   obj.keyframe_insert(data_path='location')
  
 


