---
layout: page
title: Digital Twins and Physics-Informed Learning
description: Virtual models of bridges and dams that stay in step with monitoring data, and physics-guided machine learning to predict how structures vibrate.
importance: 4 # order on the Research page (1 = first)
category: research
related_publications: true # lists the papers cited below at the bottom of the page
---

<!--
  HOW TO EDIT THIS PAGE: see the note at the top of 1_traffic_load_identification.md.
-->

A digital twin is a virtual model of a real structure that is kept up to date with live
monitoring data. It shows the current state of the structure and helps predict how it
will behave.

This research builds digital twins of bridges driven by real-time traffic load. It also
develops machine learning methods guided by physics to predict how bridges and cables
vibrate.

## Digital twins

- **Digital twin of a group of bridges,** based on machine-vision fusion monitoring of
  bridge traffic load {% cite dan2021digital %}.
- **Stream computing engine** that computes the virtual dynamic response of a bridge
  digital twin under real-time traffic load: framework and experimental validation
  {% cite dan2025novel %}.
- **Remote dam monitoring:** a digital twinning framework using the Internet of Things
  {% cite singh2026digital %}.

## Physics-informed and data-driven structural dynamics

- **VIV-SDE-Net:** a physics-informed neural framework for long-horizon prediction of
  vortex-induced vibrations (VIV) of bridges {% cite ge2026viv %}.
- **Predicting VIV of suspension bridges** with Gaussian process regression, driven by
  real bridge monitoring data {% cite dan2025gaussian %}.
- **Physics-informed neural networks** for the free vibration response of cables,
  including bending stiffness {% cite dan2025physics %}.
- **Crowdsensing-based modal analysis:** a physics-guided, mobility-conditioned Fourier
  Neural Operator that corrects pedestrian-induced distortion in crowdsensing-based
  operational modal analysis {% cite luleci2026physics %}.
- **Modal parameter identification** in the time domain from a single-channel vibration
  response, based on mode decomposition {% cite yu2023time %}.

Many of these digital twins use the traffic load data described in
[Traffic Load Identification](/projects/1_traffic_load_identification/).
