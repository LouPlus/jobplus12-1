{% extends "base.html" %}
{% from "macros.html" import render_pagination, render_company %}


{% block title %}
Company
{% endblock %}


{% block body %}
<div id="filterBox">
    filter
</div>


<div class="company-list">
    {% for company in pagination.items %}
        {{ render_company(company) }}
    {% endfor %}
</div>


{{ render_pagination(pagination, 'company.index') }}
{% endblock %}