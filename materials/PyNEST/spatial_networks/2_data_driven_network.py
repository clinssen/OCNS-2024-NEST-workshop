# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # PyNEST – Visual Cortex Model

# **Modeling networks of spiking neurons with spatial connectivity using NEST**
#
# **CNS 2022, 16.07.2022**
#
# **Tutor: [Jasper Albers](mailto:j.albers@fz-juelich.de)**

# <table><tr>
# <td> 
#     <div style="text-align:center">
#         <img src="img/balaram_2014.png" alt="histology" width="150" align="center"/> <br />
#     Balaram et al. (2014): Histological features of layers and sublayers in cortical visual areas V1 and V2 of chimpanzees, macaque monkeys, and humans </div>
# </td>
#    
# <td> 
#     <img width="200"/>
# </td>
#     
# <td> 
#     <div style="text-align:center">
#         <img src="img/potjans_2014.png" alt="flow of activity" width="400" align="center"/> <br />
#     Potjans and Diesmann (2014): The Cell-Type Specific Cortical Microcircuit: Relating Structure and Activity in a Full-Scale Spiking Network Model </div>
# </td>
#     
# </tr></table>

# In this notebook we will construct a simple model of visual cortex using spatial connectivity and a data-driven approach. We want to include the first two stages of visual processing, modeling four neuronal populations: excitatory and inhibitory neurons of both layer 4 and layer 2/3. The former is associated with receiving input from lower cortical areas; in the case of the primary visual cortex, this can be the thalamus relaying information from the retina. The latter is the main target of layer 4 neurons.

# <div style="text-align:center">
#         <img src="img/visual_cortex_model.png" alt="histology" width="650" align="center"/> <br />
#     Architecture of our network model of visual cortex. </div>

# +
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib notebook

# import NEST & NEST rasterplot
import nest
import nest.raster_plot


# -

def beautify_plot(title=None, fig=None):
    plt.xticks([-0.5, 0, 0.5])
    plt.xlabel('cortical space x [mm]')
    plt.yticks([-0.5, 0, 0.5])
    plt.ylabel('cortical space y [mm]')
    plt.xlim(-0.5,0.5)
    plt.ylim(-0.5,0.5)
    if title:
        plt.title(title, figure=fig)


# ___
# ## Setup

# ### Define parameters

# #### Simulation parameters

simtime = 5000.            # simulation time (ms)

# #### Network parameters
#
# We now want to employ a data-driven approach, using data from experimental studies of the brain that report, e.g., neuron and synapse densities as well as termination patterns for specifying the connectivity.

populations = ['L2/3E', 'L2/3I', 'L4E', 'L4I']
scaling = 0.1    # scaling down the true number of neurons

# +
num_neurons_all_layers = np.load('data/num_neurons_V1_1mm2.npy') # number of neurons per 1mm2 in macaque V1

num_neurons_all_layers *= scaling

num_neurons = {
    'L2/3E': int(num_neurons_all_layers[0, 0]),
    'L2/3I': int(num_neurons_all_layers[0, 1]),
    'L4E': int(num_neurons_all_layers[1, 0]),
    'L4I': int(num_neurons_all_layers[1, 1])
}
# -

# Rather than using indegrees, we use pre-computed connection probabilities between all four populations of the model. Computing these probabilities a task of its own as different tracing studies have to be combined. Here, we simply assume this work has already been done as we want to focus on the model building.

connection_probs = np.load('data/connection_probs.npy')    # connection probabilities, index: [target, source]

# Let us have a look at how this connectivity looks like.

import seaborn as sns
fig, ax = plt.subplots()
sns.heatmap(connection_probs)
ax.set_xticklabels(populations)
ax.set_yticklabels(populations)
ax.set_xlabel('Source population')
ax.set_ylabel('Target population')
ax.set_title('Zero-distance connection probabilities')

# #### Neuron parameters

# Here, we are using neuron parameters obtained from the [Cell Type Atlas](https://celltypes.brain-map.org/data) by the Allen Institute for Brain Science which reports physiological recordings of single neurons.

neuron_params = {
    'C_m': np.exp(5.54 + 0.57**2 / 2),      # membrane capacity (pF)
    'E_L': -70.52,                          # resting membrane potential (mV)
    'V_m': -58.,                            # initial membrane potential (mV)
    'V_reset': -70.52,                      # reset membrane potential after a spike (mV)
    'V_th': -70.52 + 27.15,                 # spike threshold
    't_ref': 2.0,                           # refractory period (ms)
    'tau_m': 3.42,                          # membrane time constant (ms)
}

# #### Synapse parameters

w = 1.36 / scaling                   # excitatory synaptic weight (mV)
g = 6.                               # relative inhibitory to excitatory synaptic weight
d = 1.5                              # synaptic transmission delay (ms)

# #### External input parameters

p_rate = 8.       # external rate (spikes/s)

# ### Configure NEST

# configure kernel
nest.ResetKernel()
nest.SetKernelStatus({'rng_seed': 192873})

# ___
# ## Spatially distributed neurons 

# ### Create neurons
#
# We want to endow the neurons with the notion of space. This functionality is built right into NEST 3:

# +
# set default parameters for neurons and create neurons
nest.SetDefaults('iaf_psc_delta', neuron_params)

pos = {}
layers = {}

for pop in populations:
    
    # define positions via a distribution in space (free, grid and list possible)
    pos[pop] =  nest.spatial.free(
                    pos=nest.random.uniform(min=-0.5, max=0.5),
                    num_dimensions=2,
                    edge_wrap=True)

    # create layers of spatially distributed neurons according to position objects
    layers[pop] = nest.Create('iaf_psc_delta', num_neurons[pop], positions=pos[pop])
# -

# Below we can check what these layers look like in 2D space.

# +
plot_e = nest.PlotLayer(layers['L2/3E'], nodecolor='cornflowerblue')
beautify_plot(title='excitatory neurons of L2/3', fig=plot_e)

plot_i = nest.PlotLayer(layers['L2/3I'], nodecolor='tomato')
beautify_plot(title='inhibitory neurons of L2/3', fig=plot_i)
# -

# ### Create connections
#
# Our neurons are now arranged in 2D layers. What will happen if we use a standard, random connection method?

# synapse specification
syn = {
    'E': {'delay': d, 'weight': w},
    'I': {'delay': d, 'weight': - g * w}
}

# We now want to take the connectivity data and connect the neuronal populations according to an exponential profile:
#
# $$p(x) = p_0 e^{-x/\beta}$$
#
# where $x$ is the horizontal distance of a target neuron to the source neuron, and $\beta$ is the characteristic length of the exponential profile. We obtain $\beta$ from fitting exponential functions to the layer-specific distribution of outgoing connections measured by Sincich et al. (2001), see image at the top of notebook 1.

beta_all_layers = np.load('data/beta.npy')    # decay constant of target layers

beta = {
    'L2/3E': beta_all_layers[0, 0],
    'L2/3I': beta_all_layers[0, 1],
    'L4E': beta_all_layers[1, 0],
    'L4I': beta_all_layers[1, 1]
}

for s, source in enumerate(populations):
    for t, target in enumerate(populations):
        
        prob_distribution = nest.spatial_distributions.exponential(
                                x = nest.spatial.distance,
                                beta = beta[target])

        conn = {'rule': 'pairwise_bernoulli',
                'p': connection_probs[t, s] * prob_distribution}
        
        nest.Connect(layers[source], layers[target], conn, syn[source[-1]])

# Let's see what this connectivity actually looks like in space. 

# +
fig_e = nest.PlotLayer(layers['L4E'], nodecolor='cornflowerblue', nodesize=40)

source = layers['L4E'][3]
target_plot = nest.PlotTargets(source, layers['L4E'], fig=fig_e,
                 src_size=250, tgt_color='indigo', tgt_size=20,
                 probability_cmap='Purples')
beautify_plot(title='excitatory neurons of L4', fig=fig_e)

# +
fig_i = nest.PlotLayer(layers['L4I'], nodecolor='tomato', nodesize=80)

source = layers['L4I'][5]
target_plot = nest.PlotTargets(source, layers['L4I'], fig=fig_i,
                 src_size=250, tgt_color='indigo', tgt_size=20)

beautify_plot(title='inhibitory neurons of L4', fig=fig_i)
# -

# ## Simulate and analyze
#
# External input is again represented as Poisson input.

# +
# create poisson generator and set 'rate' to p_rate
pgen = nest.Create('poisson_generator', params={'rate': p_rate})

# create spike recorder
spikes = {}
for pop in populations:
    spikes[pop] = nest.Create('spike_recorder')
# -

# connect poisson generator using the excitatory connection weight
for pop in populations:
    nest.Connect(pgen, layers[pop], syn_spec=syn['E'])

# Recording works by connecting the populations to recording devices.

# connect excitatory / inhibitory neurons to spike recorder
for pop in populations:
    nest.Connect(layers[pop], spikes[pop])

# #### Stimulus propagation

stimulus = False

# +
if stimulus:
    stim = nest.Create('poisson_generator',
                       params={'rate': p_rate / 1.7,
                               'start': 1000.,
                               'stop': 2000.})

    nest.Connect(stim, layers['L4E'], syn_spec=syn['E'])
    nest.Connect(stim, layers['L4I'], syn_spec=syn['E'])
    
def show_stimulus():
    plt.fill_between([1000, 2000], 0, 1e5, color='mediumseagreen', alpha=0.3, label='stimulus')
    plt.legend(loc='upper right')


# -

# simulate
nest.Simulate(simtime) 

# Creating a raster plot gives a visual representation of the network activity.

# +
# raster plot of spiking activity using nest.raster_plot
nest.raster_plot.from_device(spikes['L4E'], hist=False, title='spiking activity of L4 excitatory neurons')
plt.xlim(0, 5000)
plt.ylim(num_neurons['L2/3E'] + num_neurons['L2/3I'],
         num_neurons['L2/3E'] + num_neurons['L2/3I'] + num_neurons['L4E'])
if stimulus:
    show_stimulus()

nest.raster_plot.from_device(spikes['L4I'], hist=False, title='spiking activity of L4 inhibitory neurons')
plt.xlim(0, 5000)
plt.ylim(num_neurons['L2/3E'] + num_neurons['L2/3I'] + num_neurons['L4E'],
         num_neurons['L2/3E'] + num_neurons['L2/3I'] + num_neurons['L4E'] + num_neurons['L4I'])
if stimulus:
    show_stimulus()

# +
# raster plot of spiking activity using nest.raster_plot
nest.raster_plot.from_device(spikes['L2/3E'], hist=False, title='spiking activity of L2/3 excitatory neurons')
plt.xlim(0, 5000)
plt.ylim(0, num_neurons['L2/3E'])
if stimulus:
    show_stimulus()
    
nest.raster_plot.from_device(spikes['L2/3I'], hist=False, title='spiking activity of L2/3 inhibitory neurons')
plt.xlim(0, 5000)
plt.ylim(num_neurons['L2/3E'], num_neurons['L2/3E'] + num_neurons['L2/3I'])
if stimulus:
    show_stimulus()
# -
# What happens when we set `stimulus = True` in the cell a few cells above? Does the activity propagate to layer 2/3 even though the stimulus only targets layer 4?
# Note: "Restart kernel and re-run the whole notebook" after setting `stimulus = True`.

