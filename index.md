<script src="moment.js"></script>
<script src="moment-timezone-with-data.js"></script>

Schedule

<script>
var start_time = moment.tz("2020-07-18 12:00", "Europe/Berlin");
</script>

<script>document.write(start_time.format("Z"));</script>

12:00 Welcome and introduction to the NEST Initiative
12:30 Hands-on with NEST Desktop
13:30 Lunch break/social
14:00 Hands-on running NEST from Jupyter Notebooks
15:00 (break for CNS2020 keynote by Matt Botvinick)
16:15 Introduction to NESTML
16:45 Hands-on with NESTML and Jupyter Notebooks
17:15 Hands-on with balanced network exercises
17:45 Coffee break/social
18:15 Hands-on with balanced network (continued)
19:00 Closing



NEST is established community software for the simulation of spiking neuronal network models capturing the full  detail  of  biological  network  structures  [1].  The  simulator  runs  efficiently  on  a  range  of  architectures  from  laptops  to  supercomputers  [2].  Many  peer-reviewed  neuroscientific  studies have used NEST as a simulation tool over the past 20 years. More recently, it has become a reference code for research on neuromorphic hardware systems [3].This tutorial provides hands-on experience with recent improvements of NEST. In the past, starting out with NEST could be challenging for computational neuroscientists, as models and simulations had to be programmed using SLI, C++ or Python. NEST Desktop changes this: It is an entirely graphical  approach  to  the  construction  and  simulation  of  neuronal  network  models.  It  runs  installation-free in the browser and has proven its value in several university courses. This opens the  domain  of  NEST  to  the  teaching  of  neuroscience  for  students  with  little  programming  experience.NESTML complements this new interface by enhancing the development process of neuron and synapse models. Advanced researchers often want to study specific features not provided by models already available in NEST. Instead of having to turn to C++, using NESTML they can write down differential equations and necessary state transitions in the mathematical notation they are used to. These descriptions are then automatically processed to generate machine-optimised code.After a quick overview of the current status of NEST and upcoming new functionality, the tutorial works  through  a  concrete  example  [4]  to  show  how  the  combination  of  NEST  Desktop  and  NESTML can be used in the modern workflow of a computational neuroscientist.[1] Gewaltig M-O & Diesmann M (2007) NEST (Neural Simulation Tool) Scholarpedia 2(4):1430[2] Jordan J., Ippen T., Helias M., Kitayama I., Sato M., Igarashi J., Diesmann M., Kunkel S. (2018) Extremely Scalable Spiking Neuronal Network Simulation Code: From Laptops to Exascale Computers. Frontiers in Neuroinformatics 12: 2
[3] Gutzen R., von Papen, M., Trensch G., Quaglio P. Grün S., Denker M. (2018) Reproducible Neural Network Simulations: Statistical Methods for Model Validation on the Level of Network Activity Data. Frontiers in Neuroinformatics 12 (90)[4] Duarte R. & Morrison A. (2014). “Dynamic stability of sequential stimulus representations in adapting neuronal networks”, Front. Comput. Neurosci.
