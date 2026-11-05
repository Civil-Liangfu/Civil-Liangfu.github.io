---
layout: page
title: Structural Damage Detection
description: Finding damage early by combining load and response measurements with machine learning, influence lines, and acoustic signals.
importance: 2 # order on the Research page (1 = first)
category: research
related_publications: true # lists the papers cited below at the bottom of the page
---

<!--
  HOW TO EDIT THIS PAGE: see the note at the top of 1_traffic_load_identification.md.
-->

Damage, such as cracks or a loss of stiffness, changes how a structure responds to load.
The challenge is to detect these small changes in real monitoring data, where traffic,
temperature and noise also change the response all the time.

This research develops damage detection methods that use both the **input** (the load
acting on the structure) and the **output** (how the structure responds), together with
machine learning.

## Main contributions

- **Vision-based influence lines with weigh-in-motion:** detecting bridge damage from
  precise displacement influence lines measured by cameras, with vehicle loads from
  weigh-in-motion devices, validated by experiments {% cite ge2023bridge %}.
- **Input–output monitoring with transfer learning** for structural damage detection
  {% cite ge2024structural %}.
- **Domain adaptation** for bridge health monitoring, using physics-informed generative
  adversarial learning {% cite ge2024domain %}.
- **Automated crack identification** from acoustic waveforms with deep learning
  {% cite barbosh2024automated %}.
