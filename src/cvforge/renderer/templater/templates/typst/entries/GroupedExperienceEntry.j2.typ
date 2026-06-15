{# Company header #}
{
  set block(above: 0pt, below: 0.4em)
  {{ entry.company_column }}
}
{% for pos in entry._rendered_positions %}
{% if not design.entries.short_second_row %}
{% set first_row_lines = pos.date_and_location_column.splitlines()|length %}
{% if first_row_lines == 0 %} {% set first_row_lines = 1 %} {% endif %}
{% else %}
{% set first_row_lines = pos.main_column.splitlines()|length %}
{% endif %}
#regular-entry(
  [
{% for line in pos.main_column.splitlines()[:first_row_lines] %}
    {{ line|indent(4) }}

{% endfor %}
  ],
  [
{% for line in pos.date_and_location_column.splitlines() %}
    {{ line|indent(4) }}

{% endfor %}
  ],
{% if not design.entries.short_second_row %}
  main-column-second-row: [
{% for line in pos.main_column.splitlines()[first_row_lines:] %}
    {{ line|indent(4) }}

{% endfor %}
  ],
{% endif %}
)
{% endfor %}
