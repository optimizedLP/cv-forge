{% if entry._rendered_positions|length == 1 %}
{# Single position: render like a regular ExperienceEntry #}
{% set pos = entry._rendered_positions[0] %}
{% set combined_main = entry.company_column + ', ' + pos.main_column.splitlines()[0] + '\n' + pos.main_column.splitlines()[1:]|join('\n') %}
{% if not design.entries.short_second_row %}
{% set first_row_lines = pos.date_and_location_column.splitlines()|length %}
{% if first_row_lines == 0 %} {% set first_row_lines = 1 %} {% endif %}
{% else %}
{% set first_row_lines = combined_main.splitlines()|length %}
{% endif %}
{% set second_row = combined_main.splitlines()[first_row_lines:] %}
{% set second_row_state = namespace(has_highlights=false) %}
{% for line in second_row %}
{% if line.lstrip().startswith("- ") %}
{% set second_row_state.has_highlights = true %}
{% endif %}
{% endfor %}
#regular-entry(
  [
{% for line in combined_main.splitlines()[:first_row_lines] %}
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
{% else %}
{# Multiple positions: show company header + sub-entries #}
#block(above: 0pt, below: 0.4em)[{{ entry.company_column }}]
{% for pos in entry._rendered_positions %}
{% if not design.entries.short_second_row %}
{% set first_row_lines = pos.date_and_location_column.splitlines()|length %}
{% if first_row_lines == 0 %} {% set first_row_lines = 1 %} {% endif %}
{% else %}
{% set first_row_lines = pos.main_column.splitlines()|length %}
{% endif %}
{% set second_row = pos.main_column.splitlines()[first_row_lines:] %}
{% set second_row_state = namespace(has_highlights=false) %}
{% for line in second_row %}
{% if line.lstrip().startswith("- ") %}
{% set second_row_state.has_highlights = true %}
{% endif %}
{% endfor %}
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
{% endfor %}
{% endif %}
