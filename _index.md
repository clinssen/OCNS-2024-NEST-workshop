---
title: "New interfaces for teaching with NEST - CNS*2020"
---

<!-- HEADER -->
<div id="header_wrap" class="outer">
<header class="inner">
<h1 id="project_title"><span style="font-size:90% !important">New interfaces for teaching with NEST:</span></h1>
<h2 id="project_tagline">Hands-on with the NEST Desktop GUI and NESTML code generation</h2>
</header>
</div>

<!-- MAIN CONTENT -->
<div id="main_content_wrap" class="outer">
<section id="main_content" class="inner">


<link rel="stylesheet" type="text/css" media="screen" href="https://pages-themes.github.io/slate/assets/css/style.css?v=dd924ed8bde9d034c169c8f6d051bf93723eabbd">
<style>
/* class applies to select element itself, not a wrapper element */
.select-css {
    font-family: sans-serif;
    color: #444;
    line-height: 1.2;
    margin-bottom: .3em;
    padding: .6em 1.4em .5em .8em;
    max-width: 100%; /* useful when width is set to anything other than 100% */
    box-sizing: border-box;
    border: 1px solid #aaa;
    box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
    border-radius: .5em;
    -moz-appearance: none;
    -webkit-appearance: none;
    appearance: none;
    background-color: #fff;
    /* note: bg image below uses 2 urls. The first is an svg data uri for the arrow icon, and the second is the gradient. 
        for the icon, if you want to change the color, be sure to use `%23` instead of `#`, since it's a url. You can also swap in a different svg icon or an external image reference
        
    */
    background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'),
      linear-gradient(to bottom, #ffffff 0%,#e5e5e5 100%);
    background-repeat: no-repeat, repeat;
    /* arrow icon position (1em from the right, 50% vertical) , then gradient position*/
    background-position: right .7em top 50%, 0 0;
    /* icon size, then gradient */
    background-size: .65em auto, 100%;
}
/* Hide arrow icon in IE browsers */
.select-css::-ms-expand {
    display: none;
}
/* Hover style */
.select-css:hover {
    border-color: #888;
}
/* Focus style */
.select-css:focus {
    border-color: #aaa;
    /* It'd be nice to use -webkit-focus-ring-color here but it doesn't work on box-shadow */
    box-shadow: 0 0 1px 3px rgba(59, 153, 252, .7);
    box-shadow: 0 0 0 3px -moz-mac-focusring;
    color: #222; 
    outline: none;
}

/* Set options to normal weight */
.select-css option {
    font-weight:normal;
}

/* Support for rtl text, explicit support for Arabic and Hebrew */
*[dir="rtl"] .select-css, :root:lang(ar) .select-css, :root:lang(iw) .select-css {
    background-position: left .7em top 50%, 0 0;
    padding: .6em .8em .5em 1.4em;
}

/* Disabled styles */
.select-css:disabled, .select-css[aria-disabled=true] {
    color: graytext;
    background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22graytext%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'),
      linear-gradient(to bottom, #ffffff 0%,#e5e5e5 100%);
}

.select-css:disabled:hover, .select-css[aria-disabled=true] {
    border-color: #aaa;
}
</style>
<script src="moment.js"></script>
<script src="moment-timezone-with-data.js"></script>

<p style="margin-top: -1em; text-align: center; font-style: italic !important">An online tutorial at the [29th Annual Computational Neuroscience Meeting](https://www.cnsorg.org/cns-2020), July 18th, 2020</p>

## Description

NEST is established community software for the simulation of spiking neuronal network models capturing the full  detail  of  biological  network  structures  [1].  The  simulator  runs  efficiently  on  a  range  of  architectures  from  laptops  to  supercomputers  [2].  Many  peer-reviewed  neuroscientific  studies have used NEST as a simulation tool over the past 20 years. More recently, it has become a reference code for research on neuromorphic hardware systems [3].

This tutorial provides hands-on experience with recent improvements of NEST. In the past, starting out with NEST could be challenging for computational neuroscientists, as models and simulations had to be programmed using SLI, C++ or Python. NEST Desktop changes this: It is an entirely graphical approach to the  construction  and  simulation of neuronal  network  models.  It  runs  installation-free in the browser and has proven its value in several university courses. This opens the  domain  of NEST to the teaching of neuroscience for students with little programming experience.NESTML complements this new interface by enhancing the development process of neuron and synapse models. Advanced researchers often want to study specific features not provided by models already available in NEST. Instead of having to turn to C++, using NESTML they can write down differential equations and necessary state transitions in the mathematical notation they are used to. These descriptions are then automatically processed to generate machine-optimised code.

After a quick overview of the current status of NEST and upcoming new functionality, the tutorial works through a the construction of a balanced network to show how the combination of NEST Desktop and NESTML can be used in the modern workflow of a computational neuroscientist.


### Citations

[1] https://nest-simulator.readthedocs.io/

[2] Jordan J., Ippen T., Helias M., Kitayama I., Sato M., Igarashi J., Diesmann M., Kunkel S. (2018) Extremely Scalable Spiking Neuronal Network Simulation Code: From Laptops to Exascale Computers. Frontiers in Neuroinformatics 12: 2
	
[3] Gutzen R., von Papen, M., Trensch G., Quaglio P. Grün S., Denker M. (2018) Reproducible Neural Network Simulations: Statistical Methods for Model Validation on the Level of Network Activity Data. Frontiers in Neuroinformatics 12 (90)



## Schedule

<script>
var start_time = moment.tz("2020-07-18 12:00", "Europe/Berlin");

s = "<label for=\"tz-selector\">Timezone:&nbsp;</label>";
s += "<select class=\"select-css\" name=\"tz-selector\" id=\"tz-selector\" onChange=\"printTable(document.getElementById('schedule'), document.getElementById('tz-selector').value);\">";

moment.tz.names().forEach(function (item, index) {
	s += "<option value=\"" + item + "\"";
	if (item.localeCompare("Europe/Berlin") == 0) {
		s += " selected=\"selected\"";
	}
	s += ">" + item + "</option>";
});

s += "</select>";
document.write(s);

document.getElementById('tz-selector').value = "Europe/Berlin";

function printTable(el, in_tz) {
	//alert(in_tz);
	for (var i = 0; i < document.getElementsByClassName('timecell').length; ++i) {
		item = document.getElementsByClassName('timecell')[i];
		berlin_time = item.querySelector('noscript').innerHTML.replace(/^\s+|\s+$/g, '');
		//alert('old time: ' + berlin_time);
		//alert('attempted new time: ' + start_time.format("YYYY-MM-DD hh:mm:ss").slice(0, -8) + berlin_time + ":00");
		new_time = moment.tz(start_time.format("YYYY-MM-DD hh:mm:ss").slice(0, -8) + berlin_time + ":00", "Europe/Berlin").tz(in_tz);
		//alert('new time: ' + new_time.format());
		item.innerHTML = "<noscript>" + berlin_time + "</noscript>" + new_time.format('HH:mm');
	}
}
</script>

<div id="schedule" name="schedule">
<table>
<tr>
<th>Time <noscript>(Berlin<br>timezone)</noscript></th>
<th>Description</th>
</tr>
<tr>
<td class="timecell"><noscript>16:00</noscript>16:00</td>
<td>Welcome and introduction to the NEST Initiative</td>
</tr>
<tr>
<td class="timecell"><noscript>16:30</noscript>16:30</td>
<td>Hands-on with NEST Desktop</td>
</tr>
<tr>
<td class="timecell"><noscript>17:30</noscript>17:30</td>
<td>Lunch break/social</td>
</tr>
<tr>
<td class="timecell"><noscript>18:00</noscript>18:00</td>
<td>Hands-on running NEST from Jupyter Notebooks</td>
</tr>
<tr>
<td class="timecell"><noscript>19:00</noscript>19:00</td>
<td>(break for CNS2020 keynote by Matt Botvinick)</td>
</tr>
<tr>
<td class="timecell"><noscript>20:15</noscript>20:15</td>
<td>Introduction to NESTML</td>
</tr>
<tr>
<td class="timecell"><noscript>20:45</noscript>20:45</td>
<td>Hands-on with NESTML and Jupyter Notebooks</td>
</tr>
<tr>
<td class="timecell"><noscript>21:15</noscript>21:15</td>
<td>Hands-on with balanced network exercises</td>
</tr>
<tr>
<td class="timecell"><noscript>21:45</noscript>21:45</td>
<td>Coffee break/social</td>
</tr>
<tr>
<td class="timecell"><noscript>22:15</noscript>22:15</td>
<td>Hands-on with balanced network (continued)</td>
</tr>
<tr>
<td class="timecell"><noscript>23:00</noscript>23:00</td>
<td>Closing</td>
</tr>
</table>
</div>

## Links

<div style="text-align:center">[<img src="https://nest-simulator.readthedocs.io/en/nest-2.20.1/_static/img/nest_logo.png" border="0">](https://nest-simulator.readthedocs.io/)<br>[<span style="font-size:120%; font-weight: 120%">NEST Simulator</span>](https://nest-simulator.readthedocs.io/)</div>

<p>NEST Simulator is a spiking neuron simulator which specialises in point neurons and neurons with few comparments. It can simulate synaptic plasticity, structural plasticity, gap junctions and countless other features on machines ranging from home PCs to high-performance computing systems.</p>

<div style="text-align:center">[<img src="https://nest-desktop.readthedocs.io/en/latest/_images/nest-desktop-logo.png" border="0" width="240" height="222">](https://nest-desktop.readthedocs.io/)<br>[<span style="font-size:120%; font-weight: 120%">NEST Desktop</span>](https://nest-desktop.readthedocs.io/)</div>

<p>NEST Desktop is a web-based GUI application for NEST Simulator. It enables the rapid construction, parametrization, and instrumentation of neuronal network models.</p>

<div style="text-align:center">[<img src="https://nestml.readthedocs.io/en/latest/_static/nestml-logo.png" border="0" width="240" height="73">](https://nestml.readthedocs.io/)<br>[<span style="font-size:120%; font-weight: 120%">NESTML</span>](https://nestml.readthedocs.io/)</div>

<p> NESTML is a domain-specific modeling language and code-generation toolchain. It supports the specification of neuron models in an intuitive and concise syntax. Optimised code generation for the target simulation platform couples a highly accessible language with good simulation performance.</p>


## Registration

Please don't forget to register for the conference. Registration is free at [https://www.cnsorg.org/cns-2020](https://www.cnsorg.org/cns-2020).


## Connection details

To allow for interactive sessions, tutorials will run as “virtual rooms” (i.e. video calls) in CNS*2020. The platform is [Zoom](https://zoom.us/). It can run in your browser, and no account or installation is required. In some cases, installing the software on your local computer can improve the quality of the video and audio.

Tutorials are not recorded and are not livestreamed events on YouTube.

**The link for the tutorial video stream has been announced on the [Sched instance for CNS*2020](https://cns2020online.sched.com)**


## Software requirements

We will provide login details for virtual machines on Human Brain Project (EBRAINS) infrastructure to registered participants. You will be able to access the required software directly from your browser, without requiring any installation. Access is provided to a NEST Desktop instance, as well as a [JupyterHub](https://jupyterhub.readthedocs.io/) environment that includes NEST Simulator and NESTML.

You can also run the software on a local computer. We suggest using two Docker images that we provide:

* [Jupyter Notebook server with NEST and NESTML support](https://github.com/clinssen/OCNS-2020-workshop/tree/master/docker_containers/nest-nestml-jupyterlab-ocns-tutorial)

  Launches a Jupyter Notebook server on localhost at port 7003.

  The image is available via DockerHub. To install:

  ```
  docker pull clifzju/nest-nestml-jupyterlab-ocns-tutorial
  ```

  Then run the image while forwarding the port:

  ```
  docker run -i -d -p 7003:7003 -t clifzju/nest-nestml-jupyterlab-ocns-tutorial
  ```

  You can then access the server in your browser by navigating to the URL [http://localhost:7003](http://localhost:7003).

  The Docker container can be started in interactive mode (giving you a shell prompt) by omitting the ``-d`` parameter.

* [NEST Desktop server](https://nest-desktop.readthedocs.io/en/latest/deployer/deploy-docker.html?highlight=docker)

  For local installation, we recommend to use the official NEST Desktop Docker image and instructions. Full instructions can be found at: [https://nest-desktop.readthedocs.io/en/latest/deployer/deploy-docker.html?highlight=docker](https://nest-desktop.readthedocs.io/en/latest/deployer/deploy-docker.html?highlight=docker).

  The image is available via DockerHub. To install:

  ```
  docker pull babsey/nest-desktop
  ```

  Then run the image while forwarding the ports:

  ```
  docker run -i -p 5000:5000 -p 8000:8000 -t babsey/nest-desktop
  ```

  You can then access the server in your browser by navigating to the URL [http//localhost:8000](http://localhost:8000).


## Organisation

This tutorial is organised by, alphabetically, [Charl Linssen](https://www.fz-juelich.de/SharedDocs/Personen/IAS/JSC/EN/staff/linssen_c.html) (Forschungszentrum Jülich, Germany), [Renato Duarte](https://www.fz-juelich.de/SharedDocs/Personen/INM/INM-6/EN/staff/Duarte_Renato.html?nn=1789538) (ibid.) and [Sebastian Spreizer](https://www.uni-trier.de/index.php?id=73522&L=0) (University of Trier, Germany). For general inquiries, please contact Charl at <a href="mailto:c.linssen@fz-juelich.de">c.linssen@fz-juelich.de</a>.


## Acknowledgements

We acknowledge the use of [Fenix Infrastructure](https://fenix-ri.eu) resources, which are partially funded from the European Union's Horizon 2020 research and innovation programme through the ICEI project under the grant agreement No. 800858.

</section>
</div>

<!-- FOOTER  -->
<div id="footer_wrap" class="outer">
<footer class="inner">

<p class="copyright" style="color: #cccccc">Slate theme maintained by <a href="https://github.com/pages-themes">pages-themes</a> &bullet; Published with <a href="https://pages.github.com">GitHub Pages</a> &bullet; Timezone magic thanks to <a href="https://momentjs.com/">moment.js</a></p>
</footer>
</div>





