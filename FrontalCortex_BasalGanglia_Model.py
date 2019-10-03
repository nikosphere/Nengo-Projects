# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:42:18 2019

@author: valov
"""

import matplotlib.pyplot as plt
import numpy as np
from nengo.processes import Piecewise

import nengo


model = nengo.Network(label='Frontal Cortex and Basal Ganglia')



with model:
    frontal_units1 = nengo.Ensemble(50, dimensions=1)
    frontal_units2 = nengo.Ensemble(100, dimensions=1)
    frontal_units3 = nengo.Ensemble(100, dimensions=1)
    output = nengo.Ensemble(300, dimensions =3 , label = 'Frontal Lobe Output')
with model:
    striatal_units = nengo.Ensemble(100,dimensions=3)
    striatal_units2 = nengo.Ensemble(100,dimensions=3)
    striatal_units3 = nengo.Ensemble(100,dimensions=3)
    output2 = nengo.Ensemble(300, dimensions = 3,label = 'Striatal Output')

with model:
    sin = nengo.Node(output = np.sin)
    cos = nengo.Node(output= np.cos)
    inhib = nengo.Node(Piecewise({0: 0, 2.5: 1, 5: 0, 7.5: 1, 10: 0, 12.5: 1}))

with model:
    nengo.Connection(sin, frontal_units1)
    nengo.Connection(cos, frontal_units2)
    nengo.Connection(sin, frontal_units3)
    
    nengo.Connection(frontal_units1, output[1])
    nengo.Connection(frontal_units2, output[0])
    nengo.Connection(frontal_units3, output[2])

    
with model:
    nengo.Connection(output, striatal_units)
    nengo.Connection(output, striatal_units2)
    nengo.Connection(output, striatal_units3)
    nengo.Connection(inhib, striatal_units.neurons, transform=[[-2.5]]*100)
    nengo.Connection(inhib, striatal_units2.neurons, transform=[[-2.5]]*100)
    nengo.Connection(inhib, striatal_units3.neurons, transform=[[-2.5]]*100)


    nengo.Connection(striatal_units,output2)
    nengo.Connection(striatal_units3, output2)
    nengo.Connection(striatal_units2, output2)
    

with model:
    nigro_Units = nengo.Ensemble(100,dimensions = 3)
    nigro_Units2 = nengo.Ensemble(100, dimensions = 3)
    nigro_Units3 = nengo.Ensemble(100, dimensions = 3)
    output3 = nengo.Ensemble(300, dimensions = 3, label = 'NigroStriatal Output')

with model: 
    nengo.Connection(output2, nigro_Units)
    nengo.Connection(output2, nigro_Units2)
    nengo.Connection(output2,nigro_Units3)
    nengo.Connection(inhib, nigro_Units3.neurons, transform=[[-2.5]]*100)
    nengo.Connection(inhib, nigro_Units2.neurons, transform=[[-2.5]]*100)
    nengo.Connection(inhib, nigro_Units.neurons, transform=[[-2.5]]*100)

    nengo.Connection(nigro_Units, output3)
    nengo.Connection(nigro_Units2, output3)
    nengo.Connection(nigro_Units3, output3)

with model:
    thalamic_Units = nengo.Ensemble(300, dimensions = 3)
    output4 = nengo.Ensemble(300, dimensions = 3, label = 'Thalamus')

with model:
    nengo.Connection(output3, thalamic_Units)
    nengo.Connection(thalamic_Units, output4)
    
    nengo.Connection(output4[0],frontal_units1)
    nengo.Connection(output4[1],frontal_units2)
    nengo.Connection(output4[2],frontal_units3)

    
with model:
    sin_probe = nengo.Probe(sin)
    cos_probe = nengo.Probe(cos)
    inhib_probe = nengo.Probe(inhib)
    frontal_units1_probe = nengo.Probe(frontal_units1, synapse=0.01)
    frontal_units2_probe = nengo.Probe(frontal_units2, synapse=0.01)
    frontal_units3_probe = nengo.Probe(frontal_units3, synapse=0.01)
    out_probe = nengo.Probe(output, synapse = 0.01)
    out2_probe = nengo.Probe(output2, synapse = 0.01)
    out3_probe = nengo.Probe(output3,synapse = 0.01)
    out4_probe = nengo.Probe(output4, synapse = 0.01)
with nengo.Simulator(model) as sim:
    # Run it for 10 seconds
    sim.run(10)
    
plt.figure(1)
plt.plot(sim.trange(), sim.data[out_probe][:, 0], 'b', label="2D output")
plt.plot(sim.trange(), sim.data[out_probe][:, 1], 'g', label="2D output")
#plt.plot(sim.trange(), sim.data[out2_probe][:,0], 'r', label="out2")
#plt.plot(sim.trange(), sim.data[out2_probe] [:,1], 'y',label = "out2")
#plt.plot(sim.trange(), sim.data[out2_probe] [:,2], 'k',label = "out2")
plt.plot(sim.trange(), sim.data[out3_probe][:,0], 'y', label = "out3")
plt.plot(sim.trange(), sim.data[out3_probe][:,1], 'r', label = "out3")
plt.plot(sim.trange(), sim.data[out3_probe][:,2], 'k', label = "out3")


plt.plot(sim.trange(), sim.data[sin_probe], 'k', label="Sine")
plt.legend()

plt.figure(2)
plt.plot(sim.trange(), sim.data[out4_probe][:,0], 'g', label = "out4")
plt.plot(sim.trange(), sim.data[out4_probe][:,1], 'g', label = "out4")
plt.plot(sim.trange(), sim.data[out4_probe][:,2], 'r', label = "out4")
plt.plot(sim.trange(), sim.data[inhib_probe], 'k', label = "inhib input")
plt.legend()