---
layout: page
title: News
description: Announcements and updates, newest first.
permalink: /news/
nav: true
nav_order: 4
---

<!-- _pages/news.md: the list itself is _includes/news.liquid (news items are the files in _news/) -->

{% if site.data.socials.linkedin_username %}

<div class="home-actions news-follow">
  <a class="btn-site" href="https://www.linkedin.com/in/{{ site.data.socials.linkedin_username }}" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-linkedin"></i> Follow me on LinkedIn</a>
</div>

{% endif %}

{% include news.liquid %}
