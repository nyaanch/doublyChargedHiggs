import ROOT
import numpy as np
import re
from array import array

# Function to search among the mess in PYTHIA8 log file
def search (particle_name, file_name):

	select = re.compile('.* PYTHIA Event Listing .*')
	event_type = 'complete event'
#	particle_name = re.compile('.*\(' + particle_name +'\).*')
	particle_name = re.compile('.*' + particle_name +'.*')
	
	ok = False
	
	particle_data = []
	
	# Find all the lines that contain the name of particle
	# Open PYTHIA log file and read content
	for line in open(file_name):
		for match_select in re.finditer(select, line):
			if event_type in match_select.group(): ok = True
			
		if ok:
			for match_name in re.finditer(particle_name, line):
				particle_data.append(match_name.group().split())

		if ok and 'End PYTHIA Event Listing' in line: ok = False

	return particle_data

# Create a ROOT file and a TTree to store the data
root_file = ROOT.TFile("data.root", "RECREATE")
tree = ROOT.TTree("tree", "Tree with data from PYTHIA")

# Enter name of particle you want to search for
particle_name = 'p\+'

# Enter file name of PYTHIA8 log
file_name = "pythia.log"

# Array to store the data from PYTHIA log
test_array = []
test_array = search(particle_name, file_name)

# Create array to fill the tree 

# data = np.array([0], dtype = float) --> possible to use numpy (to speed up the calculations)
# data = np.zeros(1, dtype=float)

event = array('i', [0])
particle_id = array('i', [0])
px = array('d', [0]) 
py = array('d', [0]) 
pz = array('d', [0]) 
e = array('d', [0])
m = array('d', [0])

# Create a branch in the tree for the data
#tree.Branch("event", event, "event/I")
#tree.Branch("particle_id", particle_id, "particle_id/I")
tree.Branch("px", px, "px/D")
tree.Branch("py", py, "py/D")
tree.Branch("pz", pz, "pz/D")
tree.Branch("e", e, "e/D")
tree.Branch("m", m, "m/D")

# Create canvas and histogram
#canvas = ROOT.TCanvas("canvas", "Test Histogram", 800, 600)
#hist = ROOT.TH1D("hist", "Test histogram", 100, 0.0, 5000.0)

# Loop over the data and fill the tree
print(len(test_array))

for row in test_array:
	#print(row)

	# Fill the data array with the data from the log file
	px[0] = float(row[-5])
	py[0] = float(row[-4])
	pz[0] = float(row[-3])
	e[0] = float(row[-2])
	m[0] = float(row[-1])
	
	tree.Fill()
	print(e)

print(len(row))

# Write the tree to the ROOT file
tree.Write()

# Close the ROOT file
root_file.Close()


# =================== NOTES ===================

# maybe it iis better to use numpy arrays instead of python arrays
# https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-text-file-with-numpy-and-store-data-in-a-numpy-arr

# problem with the tree filling (only one value is stored in the tree)?? --> solved 
# https://root-forum.cern.ch/t/only-one-value-is-stored-in-the-tree/20192/2

# use git to store the code 
# https://www.youtube.com/watch?v=0fKg7e37bQE

# ask Kenneth about the kinematics of the particles (momentum, energy, mass), how to calculate the enegy loss of the particles
# https://en.wikipedia.org/wiki/Particle_kinematics

