import pytest
from dash import dcc, html
from appfile.task_3 import create_dash_app, update_graphs

@pytest.fixture
def app():
    return create_dash_app()

def test_layout_structure(app):
    layout = app.layout
    assert isinstance(layout, html.Div)

    # Ensure both graphs exist
    graph_ids = [comp.id for comp in layout.children if isinstance(comp, dcc.Graph)]
    assert "line-graph" in graph_ids
    assert "scatter-graph" in graph_ids

def test_component_types(app):
    layout = app.layout

    # Check region selector (RadioItems)
    region_selector = next(
        (comp for comp in layout.children if isinstance(comp, dcc.RadioItems)), None
    )
    assert region_selector is not None, "Region selector RadioItems not found"
    assert region_selector.id == "region-selector"

    # Check date picker
    date_picker = next(
        (comp for comp in layout.children if isinstance(comp, dcc.DatePickerRange)), None
    )
    assert date_picker is not None, "Date picker not found"

def test_callback_logic():
    # Call update_graphs directly
    line_fig, scatter_fig, msg = update_graphs("all", "2021-01-01", "2021-12-31")

    # Ensure we get valid figures back
    assert line_fig is not None
    assert scatter_fig is not None
    assert isinstance(msg, str)
