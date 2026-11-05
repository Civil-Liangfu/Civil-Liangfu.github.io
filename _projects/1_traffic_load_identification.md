---
layout: page
title: Traffic Load Identification
description: Who is on the bridge, where, and how heavy? Combining weigh-in-motion sensors with machine vision to map the traffic load on a whole bridge.
importance: 1 # order on the Research page (1 = first)
category: research
related_publications: true # lists the papers cited below at the bottom of the page
---

<!--
  HOW TO EDIT THIS PAGE
  - Write normal text. Keep the "---" header block above as it is.
  - To cite a paper, copy one of the "cite" tags used below and change the key.
    The key is the first word of the paper's entry in _bibliography/papers.bib
    (e.g. ge2020accurate). Cited papers are listed at the bottom of the page.
  - To add a picture: upload it to assets/img/ and add a line like
    ![Short description](/assets/img/your_picture.jpg)
-->

Traffic is the main everyday load on most bridges. To judge whether a bridge is safe,
engineers need to know how many vehicles are on it, where they are, and how heavy they
are, at every moment. Weigh-in-motion (WIM) sensors can weigh vehicles, but only at one
point on the road. Cameras can follow vehicles along the whole deck, but cannot weigh them.

This research combines the two. Vehicles are weighed by WIM sensors and then tracked
across the bridge with cameras and deep-learning object detection. The result is the
traffic load on the whole bridge, over time.

## Main contributions

- **Fusing WIM and multi-camera vision** to identify moving loads on a bridge
  {% cite dan2019identification %}.
- **Full-bridge load monitoring with YOLO-v3:** an accurate and robust method to monitor
  how traffic load is distributed over the whole bridge {% cite ge2020accurate %}.
- **Real-time safety checks:** using the identified positions of moving loads to monitor
  and evaluate the overturning risk of single-column-pier box-girder bridges
  {% cite ge2020real %}.
- **Traffic load simulation** that combines machine vision and WIM monitoring
  {% cite ge2022intelligent %}.
- **Long-term monitoring of long-span bridges** with an improved system for full-bridge
  traffic load distribution {% cite ge2023improved %}.
- **A benchmark dataset** for vision-based traffic load monitoring on a cable-stayed
  bridge {% cite ge2024benchmark %}.

The traffic load data from this work also drives the bridge digital twins described in
[Digital Twins and Physics-Informed Learning](/projects/4_digital_twins/).
