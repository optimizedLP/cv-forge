import pytest

from cvforge.renderer.markdown import generate_markdown
from cvforge.schema.models.cvforge_model import RenderCVModel


@pytest.mark.parametrize("cv_variant", ["minimal", "full"])
def test_generate_markdown(
    compare_file_with_reference,
    cv_variant: str,
    request: pytest.FixtureRequest,
):
    base_model = request.getfixturevalue(f"{cv_variant}_cvforge_model")

    model = RenderCVModel(
        cv=base_model.cv,
        locale=base_model.locale,
        settings=base_model.settings,
    )

    def generate_file(output_path):
        model.settings.render_command.markdown_path = output_path
        generate_markdown(model)

    reference_filename = f"{cv_variant}.md"
    assert compare_file_with_reference(generate_file, reference_filename)
