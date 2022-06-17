import lifesim
import numpy as np
import matplotlib.pyplot as plt

# ---------- Reading the Results ----------
# import a previously saved catalog
bus_read = lifesim.Bus()
bus_read.data.options.set_scenario('baseline')
bus_read.data.import_catalog(input_path='C:/Users/kervy/Desktop/LIFEmission/LIFEsim/DataTest1.hdf5')

# retrieve the DataFrame object we will use
df = bus_read.data.catalog

# ---------- Question ----------
# How many planets in the habitability zone around
# M-type stars do we predict will LIFE find?

# retrieve all M-type planets
mask_mtype = df.stype == 4
# keep only if (detected)AND(in HZ)
mask = np.logical_and.reduce((df.detected, df.habitable, mask_mtype))
# sum and divide by 500 to factor out the 500 simulated universes
result_number = mask.sum()/500.0
print('\n Number of planets in the HZ around M-type stars:', result_number, '\n')

# compare the amount of detected in HZ vs. not in HZ
selected_type = df[(df.stype == 4) & (df.detected == True)]
nb_HZvsNoHZ = selected_type.value_counts(selected_type['habitable'])/500
print("Detected M-type planet in the HZ \n", nb_HZvsNoHZ)

# view as a bar plot
# nb_HZvsNoHZ.plot.bar()
# plt.xlabel("Planet in the HZ")
# plt.ylabel("Number of detected planets around M-type star")
# plt.show()
# plt.savefig('C:/Users/kervy/Desktop/LIFEmission/LIFEsim/MtypeDetectionHZ.jpg')

# ---------- General Analysis ----------
# TO DO: implement treatment of parameter delta

# 1.1 number of detectable planets for all types of stars
nb_detected = []
for star_type in list(range(0, 5)):
    stype_selection = ((df.stype == star_type) & (df.detected == True))
    nb_detected.append(stype_selection.sum()/500)

# 1.2 number of detectable planets in HZ for all types of stars
nb_detHZ = []
for star_type in list(range(0, 5)):
    stype_selection = ((df.stype == star_type) & df.detected & df.habitable)
    nb_detHZ.append(stype_selection.sum()/500)

x = np.array(["A", "F", "G", "K", "M"])
y1 = np.array(nb_detected)
y2 = np.array(nb_detHZ)
plt.bar(x, y1)
plt.bar(x, y2)
plt.title("Number of detected planets for different stellar types")
plt.ylabel("Detectable planets")
leg = ["Detected", "Detected and in HZ"]
plt.legend(leg, loc=2)
plt.savefig(r'C:\Users\kervy\Desktop\LIFEmission\LIFEsim\StypeDetection.png', dpi=300)
plt.show()



import lifesim
import numpy as np
import matplotlib.pyplot as plt

bus_read = lifesim.Bus()

# this line does not change the file to be read, right?
bus_read.data.options.set_scenario('baseline')

# change to the optimization scenario maximizing the total number of detectable planets
bus_read.data.options.set_manual(habitable=False)

# After every planet is given an SNR, we want to distribute the time available in the search phase
# such that we maximize the number of detections.

# optimizing the result
opt = lifesim.Optimizer(name='opt')
bus_read.add_module(opt)
ahgs = lifesim.AhgsModule(name='ahgs')
bus_read.add_module(ahgs)

bus_read.connect(('transm', 'opt'))
bus_read.connect(('inst', 'opt'))
bus_read.connect(('opt', 'ahgs'))

opt.ahgs()

bus_read.data.import_catalog(input_path='C:/Users/kervy/Desktop/LIFEmission/LIFEsim/DataTest1.hdf5')

# retrieve the DataFrame object we will use
df = bus_read.data.catalog