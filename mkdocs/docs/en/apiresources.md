# API Resources 

{% set cell_heaad_style = "display: table-cell; font-weight: bold; color: #4050AA" %}
{% set cell_style = "display: table-cell; border-top: 1px solid #4050AA" %}

<div style="display: table; border-collapse: collapse; width: 100%">
  <div style="display: table-row">
    <div style="{{ cell_heaad_style }}">Kind</div>
    <div style="{{ cell_heaad_style }}">Group Version</div>
    <div style="{{ cell_heaad_style }}">Namespaced</div>
  </div>
{% for r in queryddb(sql.query.apiresources) -%}
  <div style="display: table-row">
    <div style="{{ cell_style }}">{{ r[0] }}</div>
    <div style="{{ cell_style }}">{{ r[1] }}</div>
    <div style="{{ cell_style }}">{{ r[2] }}</div>
  </div>
{% endfor %}
</div>

{{ hide_secondary_side_bar }}


