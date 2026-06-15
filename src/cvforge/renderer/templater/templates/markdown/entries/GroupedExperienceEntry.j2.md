## {{ entry.company_column.splitlines()[0] }}

{% for pos in entry._rendered_positions %}
### {{ pos.main_column.splitlines()[0] }}

{% for line in pos.date_and_location_column.splitlines() %}
{{ line }}

{% endfor %}
{% for line in pos.main_column.splitlines()[1:] %}
{%- if line != "!!!" -%}{{ line|replace("    ", "") }}
{% endif -%}
{% endfor %}

{% endfor %}
