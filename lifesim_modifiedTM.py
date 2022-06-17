import lifesim
import numpy as np

# MODIFIED TRANSMISSION MAP
# ---------- Set-Up ----------

# create bus
bus = lifesim.Bus()

# setting the options
bus.data.options.set_scenario('pessimistic')
# changing to optimization scenario 1
bus.data.options.optimization['habitable'] = False

# set options manually
# bus.data.options.set_manual(diameter=4.)

# ---------- Loading the Catalog ----------

bus.data.catalog_from_ppop(input_path='C:/Users/kervy/Desktop/LIFEmission/LIFEsim/docs/_static/baselineSample.fits')
bus.data.catalog_remove_distance(stype=0, mode='larger', dist=0.)  # remove all A stars
bus.data.catalog_remove_distance(stype=4, mode='larger', dist=10.)  # remove M stars > 10pc to
# speed up calculation

# ---------- Creating the Instrument ----------

# create modules and add to bus
instrument = lifesim.Instrument(name='inst')
bus.add_module(instrument)

transm = lifesim.TransmissionMap(name='transm')
bus.add_module(transm)

exo = lifesim.PhotonNoiseExozodi(name='exo')
bus.add_module(exo)
local = lifesim.PhotonNoiseLocalzodi(name='local')
bus.add_module(local)
star = lifesim.PhotonNoiseStar(name='star')
bus.add_module(star)

# connect all modules
bus.connect(('inst', 'transm'))
bus.connect(('inst', 'exo'))
bus.connect(('inst', 'local'))
bus.connect(('inst', 'star'))

bus.connect(('star', 'transm'))

# ---------- Creating the Optimizer ----------
# After every planet is given an SNR, we want to distribute the time available in the search phase
# such that we maximize the number of detections.

# optimizing the result
opt = lifesim.Optimizer(name='opt')
bus.add_module(opt)
ahgs = lifesim.AhgsModule(name='ahgs')
bus.add_module(ahgs)

bus.connect(('transm', 'opt'))
bus.connect(('inst', 'opt'))
bus.connect(('opt', 'ahgs'))

# parameter accounting for the non-perfect nulling
delta_ = np.insert(np.logspace(-10, -1, num=10, base=10), 0, 0, axis=0)
for val in delta_:
    print(val)
    # set the value for delta to be used in the simulation
    bus.data.options.set_manual(delta=val)

    # ---------- Running the Simulation ----------

    # run simulation. This function assigns every planet an SNR for 1 hour of integration time. Since
    # we are currently only simulating photon noise, the SNR will scale with the integration time as
    # sqrt(t)
    instrument.get_snr()

    opt.ahgs()

    # ---------- Saving the Results ----------

    bus.data.export_catalog(output_path=f'C:/Users/kervy/Desktop/LIFEmission/LIFEsim/SavedData/S1DataPessimisticTM_delta={val}.hdf5')
