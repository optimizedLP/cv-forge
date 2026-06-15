{% if entry._rendered_positions|length == 1 %}
{# Single position: render like a regular ExperienceEntry with company+position on same line #}
{% set pos = entry._rendered_positions[0] %}
{% set first_line = entry.company_column + ', ' + pos.main_column.splitlines()[0] %}
{% set rest_lines = pos.main_column.splitlines()[1:] %}
#regular-entry(
  [
    {{ first_line|indent(4) }}
{% if not design.entries.short_second_row %}
{% for line in rest_lines %}
    {{ line|indent(4) }}

{% endfor %}
{% endif %}
  ],
  [
{% for line in pos.date_and_location_column.splitlines() %}
    {{ line|indent(4) }}

{% endfor %}
  ],
{% if not design.entries.short_second_row %}
  main-column-second-row: [],
{% else %}
  main-column-second-row: [
{% for line in rest_lines %}
    {{ line|indent(4) }}

{% endfor %}
  ],
{% endif %}
)
{% else %}
{# Multiple positions: show company header + sub-entries #}
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
{% endif %}
