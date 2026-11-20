---
layout: page
permalink: /publications/
title: Publications
description: Journal papers and conference papers, each list newest first. # the papers come from _bibliography/papers.bib
nav: true
nav_order: 1
---

<!-- _pages/publications.md -->

{% comment %}
The papers are split into subsections by their BibTeX type, the word after "@"
in _bibliography/papers.bib (e.g. @article{ge2025deep, …):

- @article → Journal Papers
- @inproceedings, @conference, @proceedings → Conference Papers
- any other type (thesis, book chapter, …) → Other Publications, shown only if there is one
{% endcomment %}

{% assign journal_types = '@article' %}
{% assign conference_types = '@inproceedings, @conference, @proceedings' %}
{% assign other_types = '@book, @inbook, @incollection, @booklet, @manual, @phdthesis, @mastersthesis, @thesis, @techreport, @report, @misc, @unpublished, @online, @patent, @dataset, @software' %}

{% capture journal_count %}{% bibliography_count --query {{ journal_types }} %}{% endcapture %}
{% capture conference_count %}{% bibliography_count --query {{ conference_types }} %}{% endcapture %}
{% capture other_count %}{% bibliography_count --query {{ other_types }} %}{% endcapture %}

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<!-- Links to the subsections, with the number of papers in each -->

<nav class="pub-jump" aria-label="Publication types">
  {% if journal_count != '0' %}<a href="#journal-papers">Journal Papers <span>{{ journal_count }}</span></a>{% endif %}
  {% if conference_count != '0' %}<a href="#conference-papers">Conference Papers <span>{{ conference_count }}</span></a>{% endif %}
  {% if other_count != '0' %}<a href="#other-publications">Other Publications <span>{{ other_count }}</span></a>{% endif %}
</nav>

<script>
  // The search box reads the "#..." part of the address as a search term, so these
  // links scroll to their subsection without changing the address.
  document.querySelectorAll(".pub-jump a").forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.querySelector(link.getAttribute("href"));
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
</script>

<!-- Key for the colours of my name in the author lists -->

{% include author_legend.liquid %}

<div class="publications">

{% include publication_section.liquid id="journal-papers" title="Journal Papers" types=journal_types count=journal_count %}

{% include publication_section.liquid id="conference-papers" title="Conference Papers" types=conference_types count=conference_count %}

{% include publication_section.liquid id="other-publications" title="Other Publications" types=other_types count=other_count %}

</div>
