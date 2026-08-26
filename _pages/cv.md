---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% assign cv = site.data.cv %}

{% if cv.pdf.filename %}
[Download CV as PDF]({{ '/output/pdf/' | append: cv.pdf.filename | relative_url }})
{% endif %}

Education
======
{% for item in cv.education %}
* **{{ item.degree }}**, {{ item.institution }}, {{ item.year }}
  {% if item.advisor %}* Advisor: {{ item.advisor }}{% endif %}
{% endfor %}

Appointments and research experience
======
{% for item in cv.appointments %}
* **{{ item.start | date: "%B %Y" }} - {% if item.end == "present" %}Present{% else %}{{ item.end | date: "%B %Y" }}{% endif %}: {{ item.title }}**
  * {{ item.institution }}{% if item.organization %}, {{ item.organization }}{% endif %}
  {% if item.mentor %}* Faculty mentor: Professor {{ item.mentor }}{% endif %}
{% endfor %}
{% for item in cv.research_experience %}
* **{{ item.start | date: "%B %Y" }} - {{ item.end | date: "%B %Y" }}: {{ item.title }}**
  * {{ item.institution }}
  {% if item.advisor %}* Advisor: Professor {{ item.advisor }}{% endif %}
  {% if item.advisors %}* Advisors: {% for advisor in item.advisors %}Professor {{ advisor }}{% unless forloop.last %}, {% endunless %}{% endfor %}{% endif %}
{% endfor %}

Honors and awards
======
{% for item in cv.honors_and_awards %}
* **{{ item.name }} ({{ item.year }})**: Awarded by {{ item.awarded_by }}
{% endfor %}

Fellowships and scholarships
======
{% for item in cv.fellowships %}
* **{{ item.start | date: "%B %Y" }} - {% if item.end == "present" %}Present{% else %}{{ item.end | date: "%B %Y" }}{% endif %}:** {% if item.url %}[{{ item.name }}]({{ item.url }}){% else %}{{ item.name }}{% endif %}{% if item.organization %}, {{ item.organization }}{% endif %}
{% endfor %}

Service and leadership
======
{% for item in cv.service %}
* {% if item.start %}**{{ item.start | date: "%B %Y" }} - {% if item.end == "present" %}Present{% else %}{{ item.end | date: "%B %Y" }}{% endif %}:** {% endif %}{{ item.role }}, {% if item.url %}[{{ item.organization }}]({{ item.url }}){% else %}{{ item.organization }}{% endif %}
{% endfor %}

Publications
======
<ul>{% for post in site.publications %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>

Talks and presentations
======
<ul>{% for post in site.talks %}
  {% include archive-single-talk-cv.html %}
{% endfor %}</ul>

Teaching
======
<ul>{% for post in site.teaching %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>
