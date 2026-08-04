{% if not design.entries.short_second_row %}
{% set first_row_lines = entry.date_and_location_column.splitlines()|length %}
{% if first_row_lines == 0 %} {% set first_row_lines = 1 %} {% endif %}
{% else %}
{% set first_row_lines = entry.main_column.splitlines()|length %}
{% endif %}
{% set second_row = entry.main_column.splitlines()[first_row_lines:] %}
{% set second_row_state = namespace(has_highlights=false) %}
{% for line in second_row %}
{% if line.lstrip().startswith("- ") %}
{% set second_row_state.has_highlights = true %}
{% endif %}
{% endfor %}
#regular-entry(
  [
{% for line in entry.main_column.splitlines()[:first_row_lines] %}
    {{ line|indent(4) }}

{% endfor %}
  ],
  [
{% for line in entry.date_and_location_column.splitlines() %}
    {{ line|indent(4) }}

{% endfor %}
  ],
{% if not design.entries.short_second_row %}
  main-column-second-row: [
    #grid(
      columns: (1fr, {{ design.entries.date_and_location_width }}),
      column-gutter: {{ design.entries.space_between_columns }},
      [
{% if second_row_state.has_highlights %}
        #v(0.2em)

{% endif %}
{% for line in second_row %}
        {{ line|indent(8) }}

{% endfor %}
      ],
      [],
    )
  ],
{% endif %}
)
