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

# # PyNEST – Spatial Networks

# **Modeling networks of spiking neurons with spatial connectivity using NEST**
#
# **CNS 2022, 16.07.2022**
#
# **Tutor: [Jasper Albers](mailto:j.albers@fz-juelich.de)**

# <table><tr>
# <td> 
#     <div style="text-align:center">
#         <img src="img/sincich_2001.png" alt="spatial connectivity" width="1200" align="left"/> <br />
#     Sincich et al. (2001): Oriented Axon Projections in Primary Visual Cortex of the Monkey </div>
# </td>
#    
# <td> 
#     <img width="200"/>
# </td>
#     
# <td> 
#     <div style="text-align:center">
#         <img src="img/packer_2011.png" alt="exponential profile" width="300" align="center"/> <br />
#     Packer et al. (2011): Dense, Unspecific Connectivity of Neocortical Parvalbumin-Positive Interneurons: A Canonical Microcircuit for Inhibition? </div>
# </td>
#     
# </tr></table>

# In this notebook we will adapt the model of 
#
# `Brunel (2000) Dynamics of sparsely connected networks of excitatory and inhibitory spiking neurons. Journal of Computational Neuroscience 8(3):183-208`
#
# to a spatial neural network and investigate the implications on dynamics.

# +
import matplotlib.pyplot as plt
# %matplotlib notebook

# import NEST & NEST rasterplot

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

simtime = 10000.                   # simulation time (ms)

# #### Network parameters

gamma =                 # relative number of inhibitory connections
NE =                    # number of excitatory neurons (10.000 in [1])
NI =                    # number of inhibitory neurons

# #### Neuron parameters

# +
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
# -

# #### Synapse parameters

w = 1.                     # excitatory synaptic weight (mV)
g = 5.                     # relative inhibitory to excitatory synaptic weight
d = 1.5                    # synaptic transmission delay (ms)

# #### External input parameters

nu_th = V_th / (w * tau_m) # external rate needed to evoke activity (spikes/ms)
nu_ex = 2.0 * nu_th        # set external rate above threshold
p_rate = 1e3 * nu_ex       # external rate (spikes/s)

# ### Configure NEST

# configure kernel
nest.ResetKernel()

# ___
# ## Spatially distributed neurons 

# ### Create neurons
#
# We want to endow the neurons with the notion of space. This functionality is built right into NEST 3:

# +
# set default parameters for neurons and create neurons
nest.SetDefaults('iaf_psc_delta', neuron_params)

# define positions via a distribution in space (free, grid and list possible)

# create layers of spatially distributed neurons according to position objects

# -

# Below we can check what these layers look like in 2D space.

# +
plot_e = nest.PlotLayer(layer_e, nodecolor='cornflowerblue')
beautify_plot(title='excitatory neurons', fig=plot_e)

plot_i = nest.PlotLayer(layer_i, nodecolor='tomato')
beautify_plot(title='inhibitory neurons', fig=plot_i)
# -

# ### Create connections
#
# Our neurons are now arranged in 2D layers. Let's now connect them as in the original model.

# +
# synapse specification
syn_exc = {'delay': d, 'weight': w}
syn_inh = {'delay': d, 'weight': - g * w}

# connection specification
conn_inh = {'rule': 'fixed_indegree', 'indegree': CI}
# -

# Here comes our main modification: spatial connectivity!

# +
prob_distribution = 

conn_exc = {'rule': ,
            'p': prob_distribution}
# -

# Connecting the layers of neurons works just like regular NEST:



# Let's see what this connectivity actually looks like in space. 

# +
fig_e = nest.PlotLayer(layer_e, nodecolor='cornflowerblue', nodesize=80)

source = layer_e[5]
target_plot = nest.PlotTargets(source, layer_e, fig=fig_e,
                 probability_parameter=prob_distribution,
                 src_size=250, tgt_color='moccasin', tgt_size=20,
                 probability_cmap='Purples')
beautify_plot()
target_plot.get_axes()[1].set_ylabel('connection probability')

# +
fig_i = nest.PlotLayer(layer_i, nodecolor='tomato', nodesize=80)

source = layer_i[5]
target_plot = nest.PlotTargets(source, layer_i, fig=fig_i,
                 src_size=250, tgt_color='moccasin', tgt_size=20,
                 probability_cmap='Greens')
beautify_plot()
# -

# ## Simulate and analyze
#
# External input is again represented as Poisson input.

# +
# create poisson generator and set 'rate' to p_rate


# create spike recorder

# -

# connect poisson generator using the excitatory connection weight



# Recording works by connecting the populations to recording devices.

# connect excitatory / inhibitory neurons to spike recorder



# ### Run the simulation

# simulate


# Creating a raster plot gives a first glimpse of the network activity.

# raster plot of spiking activity using nest.raster_plot
nest.raster_plot.from_device(spikes_e, hist=False, title='excitatory neurons')
plt.xlim(0, 1000)
plt.ylim(0, NE)
nest.raster_plot.from_device(spikes_i, hist=False, title='inhibitory neurons')
plt.xlim(0, 1000)
plt.ylim(NE, NE+NI)

# ## Spatial activity
#
# How does the activity propagate across space?

senders = spikes_e.events['senders']
spikes = spikes_e.events['times']

import numpy as np
def instantaneous_rate(global_ids, spikes, senders, t, bin_width = 100):
    
    window = [t - bin_width / 2, t + bin_width / 2]
    rates = np.empty(len(global_ids))
    
    for i, global_id in enumerate(global_ids):
        spikes_id = spikes[senders == global_id]
        rates[i] = np.sum((window[0] < spikes_id) * (spikes_id < window[1]))
    
    return rates / bin_width * 1e3


# +
import matplotlib.animation as animation
     
def update_plot(i, data, scat, time):
    scat.set_array(data[i])
    plt.title(f'Instantaneous firing rate\n elapsed time: {int(time[i])} ms')
    return scat,

def firing_rate_over_time(neurons, spikes, senders, bin_width = 1000, delta_t = 50, interval=10,
                          spikes_with_pulse=None, senders_with_pulse=None):
    
    # extract spatial positions
    x = np.asarray(neurons.spatial['positions'])[:,0]
    y = np.asarray(neurons.spatial['positions'])[:,1]
    
    # calculate time range over which to animate
    t_range = np.arange(bin_width / 2, simtime - (bin_width / 2) + delta_t, delta_t)
    
    # calculate instantaneous rate over time range
    rate = [instantaneous_rate(layer_e.global_id, spikes, senders, t) for t in t_range]
    
    # in case pulse is given, calculate relative rate change
    if spikes_with_pulse is not None:
        rate_with_pulse = [instantaneous_rate(layer_e.global_id, spikes_with_pulse,
                                              senders_with_pulse, t) for t in t_range]
        rate_difference = []
        for i in range(len(rate)):
            rate_difference.append(rate_with_pulse[i] - rate[i])
        rate = rate_difference
        title = 'Change of instantaneous firing rate with pulse'

    # set up initial figure
    fig = plt.figure()
    scat = plt.scatter(x=x, y=y, c=rate[0], s=30)

    # animation
    ani = animation.FuncAnimation(fig, update_plot, frames=range(len(t_range)),
                                  fargs=(rate, scat, t_range), interval=interval)
    
    # add colorbar and axis labels
    plt.colorbar(label=r'$\frac{spikes}{s}$')
    plt.xlabel('cortical space x [mm]')
    plt.ylabel('cortical space y [mm]')
    
    return ani


# -

ani = firing_rate_over_time(layer_e, spikes, senders)
plt.show()

# For the spatial connectivity to have a visible effect, the recurrent connectivity needs to be stronger. See what happens when you increase the weight by a factor of 10.

# ## Further material
#
# easy-to-read guide to spatial networks in NEST: https://nest-simulator.readthedocs.io/en/latest/guides/spatial/guide_spatially_structured_networks.html
