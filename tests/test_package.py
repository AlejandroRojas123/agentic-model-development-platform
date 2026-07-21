import amdp


def test_package_is_importable() -> None:
    """Verify that the installed project package can be imported."""
    assert amdp.project_name() == "Agentic Model Development Platform"
    assert amdp.__version__ == "0.1.0"