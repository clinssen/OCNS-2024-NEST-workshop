---
title: "From single-cell modeling to large-scale network dynamics with NEST Simulator"
---

<!-- HEADER -->
<div id="header_wrap" class="outer">
<header class="inner">
<h1 id="project_title"><span style="font-size:90% !important">From single-cell modeling to large-scale network dynamics with NEST Simulator</span></h1>
<!-- <h2 id="project_tagline">No tagline here</h2> -->
</header>
</div>

<!-- MAIN CONTENT -->
<div id="main_content_wrap" class="outer">
<section id="main_content" class="inner">


<link rel="stylesheet" type="text/css" media="screen" href="https://pages-themes.github.io/slate/assets/css/style.css?v=dd924ed8bde9d034c169c8f6d051bf93723eabbd">
<style>
header {
	text-align: center
}

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

#start_date_time {
	font-weight: bold
}
</style>
<script src="moment.js"></script>
<script src="moment-timezone-with-data.js"></script>

<p style="margin-top: -1em; text-align: center; font-style: italic !important">An on-site tutorial at the [31st Annual Computational Neuroscience Meeting](https://www.cnsorg.org/cns-2022), July 16-20, 2022</p>
<p style="text-align: center; margin: -1em">—</p>
<p style="margin-top: 1em; text-align: center; font-style: italic !important">An online tutorial as a [CNS satellite event](https://ocns.github.io/SoftwareWG/pages/software-wg-satellite-tutorials-at-cns-2022.html), July 1st, 2022</p>

## Description

NEST is an established, open-source simulator for spiking neuronal networks, which can
capture a high degree of detail of biological network structures while retaining high
performance and scalability from laptops to HPC [1]. This tutorial provides hands-on
experience in building and simulating neuron, synapse, and network models. It introduces
several tools and front-ends to implement modeling ideas most efficiently. Participants do not
have to install software as all tools can be accessed via the cloud.

First, we look at NEST Desktop [2], a web-based graphical user interface (GUI), which allows
the exploration of essential concepts in computational neuroscience without the need to learn
a programming language. This advances both the quality and speed of teaching in
computational neuroscience. To get acquainted with the GUI, we will create and analyze a
balanced two-population network.
The model is then exported to a Jupyter notebook and endowed with a data-driven spatial
connectivity profile of the cortex, enabling us to study the propagation of activity. Then, we
make the synapses in the network plastic and let the network learn a reinforcement learning
task, whereby the learning rule goes beyond pre-synaptic and post-synaptic spikes by adding
a dopamine signal as a modulatory third factor. NESTML [3] makes it easy to express this and
other advanced synaptic plasticity rules and neuron models, and automatically translates
them into fast simulation code.
More morphologically detailed models, with a large number of compartments and custom ion
channels and receptor currents, can also be defined using NESTML. We first implement a
simple dendritic layout and use it to perform a sequence discrimination task. Next, we
implement a compartmental layout representing semi-independent subunits and recurrently
connect several such neurons to elicit an NMDA-spike driven network state.


### Citations

[1] https://nest-simulator.readthedocs.org/

[2] https://nest-desktop.readthedocs.org/

[3] https://nestml.readthedocs.org/


## Schedule (on-site tutorial)

<script>
var default_tz = 'Australia/Victoria';

var start_time = moment.tz("2022-07-16 09:30", "Australia/Victoria"); // !!! also update start time in the <noscript> table in plain HTML

s = "<label for=\"tz-selector\">Timezone:&nbsp;</label>";
s += "<select class=\"select-css\" name=\"tz-selector\" id=\"tz-selector\" onChange=\"printTable(document.getElementById('schedule'), document.getElementById('tz-selector').value);\">";

moment.tz.names().forEach(function (item, index) {
	s += "<option value=\"" + item + "\"";
	if (item.localeCompare(default_tz) == 0) {
		s += " selected=\"selected\"";
	}
	s += ">" + item + "</option>";
});

s += "</select>";
document.write(s);

document.getElementById('tz-selector').value = default_tz;

function printTable(el, in_tz) {
	//alert(in_tz);
	for (var i = 0; i < document.getElementsByClassName('timecell').length; ++i) {
		item = document.getElementsByClassName('timecell')[i];
		orig_time = item.querySelector('noscript').innerHTML.replace(/^\s+|\s+$/g, '');
		//alert('orig time: ' + orig_time);
		//alert('attempted new time: ' + start_time.format("YYYY-MM-DD HH:mm:ss").slice(0, -8) + orig_time + ":00");
		//alert('new time with date: ' + moment.tz(start_time.format("YYYY-MM-DD HH:mm:ss"), "Europe/Berlin").tz(in_tz).format("YYYY-MM-DD HH:mm:ss"));
		new_time = moment.tz(start_time.format("YYYY-MM-DD HH:mm:ss").slice(0, -8) + orig_time + ":00", default_tz).tz(in_tz);
		if (i == 0) {
			//alert('new time: ' + new_time.format("dddd MMMM Do, HH:mm"));
			document.getElementById('start_date_time').innerHTML = new_time.format("dddd MMMM Do, HH:mm");
		}
		//alert('new time: ' + new_time.format());
		item.innerHTML = "<noscript>" + orig_time + "</noscript>" + new_time.format('HH:mm');
	}
}

window.addEventListener('load', (event) => {
	printTable(document.getElementById('schedule'), document.getElementById('tz-selector').value);
});

</script>

The tutorial will start on <span id="start_date_time">Saturday, July 16, 09:30</span>. <!-- !!! also update start time in the JavaScript below, and in the <noscript> table in plain HTML -->

<div id="schedule" name="schedule">
<table>
<tr>
<th>Time <noscript>(Melbourne<br>timezone)</noscript></th>
<th>Description</th>
</tr>
<tr>
<td class="timecell"><noscript>09:00</noscript></td>
<td>Overview and introduction to NEST Simulator<br><span style="font-style:italic">Charl Linssen</span></td>
</tr>
<tr>
<td class="timecell"><noscript>09:30</noscript></td>
<td>Data-driven spatial plastic networks<br><span style="font-style:italic">Jasper Albers, Agnes Korcsak-Gorzo</span></td>
</tr>
<tr>
<td class="timecell"><noscript>11:00</noscript></td>
<td>Coffee break</td>
</tr>
<tr>
<td class="timecell"><noscript>11:15</noscript></td>
<td>Modeling dopamine-modulated STDP synapses with NESTML<br><span style="font-style:italic">Pooja Babu, Charl Linssen</span></td>
</tr>
<tr>
<td class="timecell"><noscript>12:30</noscript></td>
<td>Lunch break</td>
</tr>
<tr>
<td class="timecell"><noscript>13:30</noscript></td>
<td>Interactive network design with NEST Desktop<br><span style="font-style:italic">Jens Bruchertseifer, Sebastian Spreizer</span></td>
</tr>
<tr>
<td class="timecell"><noscript>14:30</noscript></td>
<td>Coffee break</td>
</tr>
<tr>
<td class="timecell"><noscript>14:45</noscript></td>
<td>Morphologically detailed models with NEST<br><span style="font-style:italic">Joshua Böttcher</span></td>
</tr>
<tr>
<td class="timecell"><noscript>16:00</noscript></td>
<td>Closing</td>
</tr>
</table>
</div>


## Links

<div style="text-align:center">[<img src="https://raw.githubusercontent.com/clinssen/OCNS-2022-workshop/master/nest_logo.png" border="0">](https://nest-simulator.readthedocs.io/)<br>[<span style="font-size:120%; font-weight: 120%">NEST Simulator</span>](https://nest-simulator.readthedocs.io/)</div>

<p>NEST Simulator is a spiking neuron simulator which specialises in point neurons and neurons with few comparments. It can simulate synaptic plasticity, structural plasticity, gap junctions and countless other features on machines ranging from home PCs to high-performance computing systems.</p>

<div style="text-align:center">[<img src="https://raw.githubusercontent.com/clinssen/OCNS-2022-workshop/master/nest-desktop-logo.png" border="0" width="240" height="222">](https://nest-desktop.readthedocs.io/)<br>[<span style="font-size:120%; font-weight: 120%">NEST Desktop</span>](https://nest-desktop.readthedocs.io/)</div>

<p>NEST Desktop is a web-based GUI application for NEST Simulator. It enables the rapid construction, parametrization, and instrumentation of neuronal network models.</p>

<div style="text-align:center">[<img src="https://raw.githubusercontent.com/clinssen/OCNS-2022-workshop/master/nestml-logo.png" border="0" width="240" height="73">](https://nestml.readthedocs.io/)<br>[<span style="font-size:120%; font-weight: 120%">NESTML</span>](https://nestml.readthedocs.io/)</div>

<p>NESTML is a domain-specific modeling language and code-generation toolchain. It supports the specification of neuron models in an intuitive and concise syntax. Optimised code generation for the target simulation platform couples a highly accessible language with good simulation performance.</p>


## Registration

Please don't forget to register for the on-site conference at [https://www.cnsorg.org/cns-2022](https://www.cnsorg.org/cns-2022).

Free online satellite tutorials are given as part of CNS*2022 between June 27th and July 1st. Registration is free but required at [https://ocns.github.io/SoftwareWG/pages/software-wg-satellite-tutorials-at-cns-2022.html](https://ocns.github.io/SoftwareWG/pages/software-wg-satellite-tutorials-at-cns-2022.html)

Tutorials are not recorded and are not livestreamed events on YouTube.

<!-- ## Connection details

To allow for interactive sessions, tutorials will run as “virtual rooms” (i.e. video calls) in CNS*2022. The platform is [Zoom](https://zoom.us/). It can run in your browser, and no account or installation is required. In some cases, installing the software on your local computer can improve the quality of the video and audio.

**The link for the tutorial video stream will been announced on the [Sched instance for CNS*2021](https://cns2021online.sched.com)**

-->

## Software requirements

We will provide login details for virtual machines on Human Brain Project (EBRAINS) infrastructure to registered participants. You will be able to access the required software directly from your browser, without requiring any installation. Access is provided to a NEST Desktop instance, as well as a [JupyterHub](https://jupyterhub.readthedocs.io/) environment that includes NEST Simulator and NESTML.

You can also run the software on a local computer. We suggest using two Docker images that we provide:

* [Jupyter Notebook server with NEST and NESTML support](https://github.com/clinssen/OCNS-2022-workshop/tree/master/docker_containers/nest-nestml-jupyterlab-ocns-tutorial)

  Launches a Jupyter Notebook server on localhost at port 7003. The password is: **nest25years**

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

* [NEST Desktop](https://nest-desktop.readthedocs.io/en/latest/deployer/deploy-docker.html)

  For local installation, we recommend to use the official NEST Desktop Docker image and instructions. Full instructions can be found at: [https://nest-desktop.readthedocs.io/en/latest/deployer/deploy-docker.html](https://nest-desktop.readthedocs.io/en/latest/deployer/deploy-docker.html).


## Feedback

If you participated in (any part) of this tutorial, we value your feedback! Please take a moment to fill in our short feedback form at [https://forms.gle/yv9MwmAKJugTs2mR9](https://forms.gle/yv9MwmAKJugTs2mR9).


## Organisation

This tutorial is organised by Charl Linssen (Jülich Research Centre, Germany), Agnes Korcsak-Gorzo (Jülich Research Centre, Germany), Jasper Albers (Jülich Research Centre, Germany), Pooja Babu (Jülich Research Centre, Germany), Joshua Böttcher (Jülich Research Centre, Germany), Jessica Mitchell (Jülich Research Centre, Germany), Willem Wybo (Jülich Research Centre, Germany), Jens Bruchertseifer (University of Trier, Germany), Sebastian Spreizer  (University of Trier, Germany) and Dennis Terhorst (Jülich Research Centre, Germany).

For general inquiries, please contact Charl at <a href="mailto:c.linssen@fz-juelich.de">c.linssen@fz-juelich.de</a>.


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




