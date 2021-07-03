
## Multi-scale brain structure and dynamics}


  
  
    
      \def\picname{scales.pdf}
      \pgfdeclareimage[interpolate=true,width=7.5cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
    }
    % \showgrid
  }



## The microcircuit model}


  
  

    
      
        \item $10^5$ identical leaky-integrate and fire neurons
        \item $3\cdot10^8$ exponentially decaying synaptic currents
        \item four layers with one excitatory and one inhibitory population each
        \item size of populations and connection probabilities deduced from anatomical data sets % for example electrophysiological recordings
      
      }}}
    
      
        \item asynchronous irregular and cell-type specific firing rates
        \item thalamic stimulation elicits flow of activity through cortical layers
      
      }}}

    
      \def\picname{column.pdf}
      \pgfdeclareimage[interpolate=true,width=3.0cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
     }

    
      \flushleft\footnotesize Potjans and Diesmann (2014) The Cell-Type Specific Cortical Microcircuit: Relating Structure and Activity in a Full-Scale Spiking Network Model. Cerebral Cortex 24(3):785-806
      }}}
  }



## The multi-area model}


  
  

    
      
        \item<1-> full-density model of macaque visual cortex
        \item axonal tracing data from the CoCoMac database, which are systematically refined using dynamical constraints
        \item stable asynchronous irregular ground state
      
      }}}
    
      
        \item produces realistic spiking statistics in V1
        \item functional connectivity compares to fMRI measurements
      
      }}}

    
      \def\picname{MAM.pdf}
      \pgfdeclareimage[interpolate=true,width=7.0cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
     }

    
      \flushleft\footnotesize Schmidt et al. (2018) Multi-scale account of the network structure of macaque visual cortex. Brain Structure and Function 223(3):1409-1435\\
      Schmidt et al. (2018) A multi-scale layer-resolved spiking network model of resting-state dynamics in macaque visual cortical areas. PLOS CB 14(10):e1006359
      }}}
  }



## Importance of the correct network size}


  
  

    
          
              \item<1-> under which conditions can a small network represent a subsampled larger network?
              \item analyzes scalability of binary and LIF neuron networks
          
        }}}
    
          
              \item mean activity can be preserved by adjusting the mean and variance of the input
              \item temporal structure of pairwise averaged correlations depends on the effective connectivity and cannot always be preserved
          
        }}}
    
      \def\picname{Albada2015.pdf}
      \pgfdeclareimage[interpolate=true,width=6.5cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
     }

    
      \flushleft\footnotesize van Albada et al. (2015) Scalability of Asynchronous Networks Is Limited by One-to-One Mapping between Effective Connectivity and Correlations. PLOS CB 11(9):e1004490
      }}}
  }



## NEST = NEural Simulation Tool}


  
  
    
          
              \item<1-> Focus on the dynamics, size and structure of neural systems rather than on the exact morphology of individual neurons
              \item<1-> NEST runs on laptops ({\footnotesize{Linux, Mac OS X ($\geq$10.3), Windows via virtualization}}) as well as supercomputers $\rightarrow$ simulations of large-scale models
              \item<1-> NEST is a hybrid parallel (OpenMP+MPI) simulator for spiking neural networks, written in C++ with a Python front end
          
        }}}

    
          
              \item<1-> Get publication and source code on http://nest-simulator.org
          
        }}}


      \def\picname{K.pdf}
      \pgfdeclareimage[interpolate=true,width=5cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
     }
  }



## Programming languages}


  
  
    
          
            \item C++ kernel
            \item Built-in simulation language interpreter (SLI)
            \item Python-based user interface (PyNEST)
          
        }}}
    
          
            \item Back end for the simulator- independent modeling tool PyNN
            \item Interface to the Multi Simulator Coordinator MUSIC
          
        }}}


    
      \begin{pgfrotateby}{\pgfdegree{270}}
      \def\picname{python_interface.pdf}
      \pgfdeclareimage[interpolate=true,width=6cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
      \end{pgfrotateby}
     }
     }



## Three main components of a NEST simulation}


  
  
    

\item \textbf{Nodes}

	\item Neurons -- Devices (-- Sub-networks)
	\item Have dynamic state variable(s) that changes over time ($V_\mathrm{m}(t)$)
	\item Can be affected by events (spikes)
	
\item \textbf{Events}
	
	\item Pieces of information of a particular type
	(e.g., spike, voltage or current event)
	\item Recording devices: \url{`spike_detector', `voltmeter', `multimeter'}
	
\item \textbf{Connections}
	
	\item Communication channels for the exchange of events
	\item Directed (from source node to target node)
	\item Weighted (how strongly does an event influence the target node)
	\item Delayed (length of transmission duration between source and target)
	\item Connections are created using one global \url{Connect} function
	

}}}
}



## NEST neuron and synapse models}


  
  
    
      \def\picname{models.pdf}
      \pgfdeclareimage[interpolate=true,width=12.3cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
     }
  }


## Event-driven vs.~time-driven simulation}

  +/-     Event-driven             Time-driven
  ------  -----------------------  -----------------------
  Pros    more efficient for low   more efficient for high
          input rates              input rates

          'correct' solution for   works for all neuron
          invertible neuron models models

                                   scales well

  Cons    only works for neurons   only `approximate'
          with invertible dynamics solution even for
                                   analytically solvable
                                   models

          event queue does not     spikes can be missed due
          scale well               to discrete sampling of
                                   membrane potential
  ------  -----------------------  -----------------------


## Event-driven vs.~time-driven simulation}

   \flushleft NEST: hybrid approach to simulation
        
        \item input events to neurons are frequent: time-driven algorithm
          
  \item If the dynamics is nonlinear, we need a numerical method to solve it,
    e.g.:
    
    \item Forward Euler: \quad $y([i+1]h)=y(ih)+h\cdot\dot{y}(ih)$
    \item Runge-Kutta ($k$th order)
    \item Runge-Kutte-Fehlberg with adaptive step size
    \item \ldots
    
   \item<1->[$\rightarrow$]
     Use a pre-implemented solver, for example, from the GNU Scientific Library (GSL).
     \\[2ex]
   \item<1->
     \alert{If the dynamics is linear (e.g.~LIF or MAT), we can solve it exactly.}

        \item events at synapses are rare: event driven component
          
          \item Exception: gap junctions

## Exact integration of linear time-invariant systems}


  \def\picname{Rotter99a_prop.pdf}
  \pgfdeclareimage[interpolate=true,width=6cm]{\picname}{\figpath\picname}
  \pgfbox[center,center]{\pgfuseimage{\picname}}

  \item consider time-invariant linear system
    \begin{math}
      \alert{\dot{y}=Ay+x}
    \end{math}\\
  \item[$\rightarrow$] \alert{exact} solution:
    \begin{math}\displaystyle
      y(t)=e^{A(t-s)}y(s)+\int_{s_+}^{t} e^{A(t-\tau)}x(\tau)\,d\tau
    \end{math}\\
  \item time grid: $\{t_k=k\cdot{}h\,|\,k=1,2,\ldots\}$;
            spike train:
    \begin{math}\displaystyle
      x(t)=\sum_k x_k\delta(t-t_k)
    \end{math}
  \item [$\rightarrow$] general solution:
    \begin{math}\displaystyle
      \alert{y_{k+1}=e^{Ah}y_k+x_{k+1}}
    \end{math}
    % integral turns into sum -> iteration, y_k is propagated and x_k+1 is added
  \item iterative propagation of solution\\[8ex]
  \item[] with  \alert{propagator} (matrix) $P(h)=e^{Ah}$

       \flushleft\footnotesize Rotter and Diesmann (1999)
       Exact digital simulation of time-invariant linear systems with applications to neuronal modeling.
       Biological Cybernetics 81(5-6):381-402



## Representation of network structure: serial}

          \item<1-> each neuron and synapse maintains its own parameters
          \item synapses save the index of the target neuron
      \def\picname{network_representation_serial.pdf}
      \pgfdeclareimage[interpolate=true,width=8cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}



## Representation of network structure: distributed}


          \item modulo operation distributes neurons
          \item one target list for every neuron on each machine
          \item synapse stored on machine that hosts the target neuron
          \item connections are established on each machine and the connectivity information subsequently propagated to other machines
              \item[$\rightarrow$] wiring is a parallelizable task
        }}}
      \def\picname{network_dist.pdf}
      \pgfdeclareimage[interpolate=true,width=5.2cm]{\picname}{\figpath\picname}
      \pgfbox[center,center]{\pgfuseimage{\picname}}
     }
    %% \showgrid
  }



## Creating custom models}

  \item Discuss with developers via user mailing list

      \item if your idea makes sense
      \item if it has not yet been implemented

  \item Only create models for NEST versions $>$ 2.10

      \item Start from most similar existing model
      \item It may end up in a release!


  %\vspace*{5mm}

  \item Extension modules (C++)

    \item loaded dynamically (recommended)
    \item \footnotesize{\url{http://nest.github.io/nest-simulator/extension_modules}}
    %\item Start from examples/MyModule
    %\item Load module: nest.Install("mymodule")
    %\item Details are about to change

  \item Inside NEST (C++)
    %
    %\item No need to load separately
    %\item Allows others to use your code
    %
  \item {\bf NESTML (NEST Modeling Language)}

    \item New simplified language with syntax similar to Python (even more recommended)
    \item Currently enables developing neuron but not yet synapse models
    %\item Plotnikov et al. "NESTML: a modeling language for spiking neurons" arXiv:1606.02882 (2016).


  %\vspace*{5mm}

  \item Re-compile and re-install after each change
  



## Topology}

  \item
    Functionality:
    
    \item
      Lay out elements on grids or at arbitrary points in space (2D or 3D)
    \item
      Elements can be neurons or combinations of neurons and devices
    \item
      Connect neurons in a position- and distance-dependent manner
    \item
      Set periodic boundary conditions
    \item
      Choose whether to allow self-connections (autapses) or multiple connections (multapses)
    \item
      Distance-dependent or random weights and delays
    
  \item
    User manual: \url{https://www.nest-simulator.org/documentation/} $\to$ Topological connections



## Why should I use NEST?}

[fragile]
      \item NEST provides over 50 neuron models
      \item NEST provides over 10 synapse models, including short-term plasticity (Tsodyks \& Markram)
      and different variants of STDP
      \item NEST provides many examples that help you getting started % with your own simulation project
      % \item NEST offers convenient and efficient commands to define and connect large networks,
      % ranging from algorithmically determined connections to data-driven connectivity
      \item NEST lets you inspect and modify the state of each neuron and each connection at any time during a simulation
      \item NEST is fast and memory efficient; it makes best use of your multi-core computer and compute clusters %with minimal user intervention
      \item NEST has a large and experienced developer community %of all neural simulators
      \item NEST was first released in 1994 under the name SYNOD and has been extended and improved ever since
      \item NEST is open source software and is licensed under the GPL 2
    



## Now hands-on}


\item{\bf Install NEST}
  			
  				\item Instructions: \url{https://www.nest-simulator.org/documentation/}
  				\item On Windows use a virtual machine (USB sticks with image available)
  				\item On Ubuntu you can also use a PPA: \url{ppa:nest-simulator/nest}
  			
\item{\bf Get the exercises}
  		
  			\item Go to \url{https://github.com/alexvanmeegen/eitn_spring_school}
  			\item Download as zip (or clone)
  		
  		\item{\bf Enjoy the ride}
  			
  				\item Open \url{0_hello_world.ipynb} for a first glance
  				\item Get going with \url{1_first_steps.ipynb}
  			

