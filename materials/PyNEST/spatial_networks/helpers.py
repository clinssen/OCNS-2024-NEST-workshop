import nest

# simulation parameters
simtime = 1000.            # simulation time (ms)
dt = 0.1                   # simulation resolution (ms)

# network parameters
gamma = 0.25               # relative number of inhibitory connections
NE = 5000                  # number of excitatory neurons (10.000 in [1])
NI = int(gamma * NE)       # number of inhibitory neurons
N_rec = 50                 # record from 100 (50 e + 50 i) neurons
CE = 1000                  # indegree from excitatory neurons
CI = int(gamma * CE)       # indegree from inhibitory neurons

# synapse parameters
w = 0.1                    # excitatory synaptic weight (mV)
g = 5.                     # relative inhibitory to excitatory synaptic weight
d = 1.5                    # synaptic transmission delay (ms)

# neuron paramters
V_th = 20.                 # spike threshold (mV)
tau_m = 20.                # membrane time constant (ms)
neuron_params = {
    'C_m': 1.0,            # membrane capacity (pF)
    'E_L': 0.,             # resting membrane potential (mV)
    'I_e': 0.,             # external input current (pA)
    'V_m': 0.,             # membrane potential (mV)
    'V_reset': 10.,        # reset membrane potential after a spike (mV)
    'V_th': V_th,          #
    't_ref': 2.0,          # refractory period (ms)
    'tau_m': tau_m,        #
}

# external input parameters
nu_th = V_th / (w * tau_m) # external rate needed to evoke activity (spikes/ms)
nu_ex = 2.0 * nu_th        # set external rate above threshold
p_rate = 1e3 * nu_ex       # external rate (spikes/s)

# configure kernel
nest.ResetKernel()
nest.SetKernelStatus({
    'resolution': dt,      # set simulation resolution
    'print_time': True,    # enable printing of simulation progress (-> terminal)
    'local_num_threads': 2 # use two threads to build & simulate the network
})

# set default parameters for neurons and create neurons
nest.SetDefaults('iaf_psc_delta', neuron_params)
neurons_e = nest.Create('iaf_psc_delta', NE)
neurons_i = nest.Create('iaf_psc_delta', NI)

# create poisson generator and set 'rate' to p_rate
pgen = nest.Create('poisson_generator', params={'rate': p_rate})

# create spike detectors
spikes_e = nest.Create('spike_recorder')
spikes_i = nest.Create('spike_recorder')

# create excitatory connections

# synapse specification
syn_exc = {'delay': d, 'weight': w}
# connection specification
conn_exc = {'rule': 'fixed_indegree', 'indegree': CE}
# connect stuff
nest.Connect(neurons_e, neurons_e, conn_exc, syn_exc)
nest.Connect(neurons_e, neurons_i, conn_exc, syn_exc)

# create inhibitory connections

# synapse specification
syn_inh = {'delay': d, 'weight': - g * w}
# connection specification
conn_inh = {'rule': 'fixed_indegree', 'indegree': CI}
# connect stuff
nest.Connect(neurons_i, neurons_e, conn_inh, syn_inh)
nest.Connect(neurons_i, neurons_i, conn_inh, syn_inh)

# connect poisson generator using the excitatory connection weight
nest.Connect(pgen, neurons_i, syn_spec=syn_exc)
nest.Connect(pgen, neurons_e, syn_spec=syn_exc)

# connect poisson generator using the excitatory connection weight
nest.Connect(pgen, neurons_i, syn_spec=syn_exc)
nest.Connect(pgen, neurons_e, syn_spec=syn_exc)