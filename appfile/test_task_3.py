import pytest
from unittest.mock import patch
import pandas as pd
from dash import dcc, html
from new.appfile.task_3 import create_dash_app, update_graphs

# Fixture to create the Dash app with mocked data
@pytest.fixture
def app():
    dummy_df = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-02"],
        "region": ["Africa", "Africa"],
        "sales": [100, 150]
    })
    with patch("new.appfile.task_3.load_data", return_value=dummy_df):
        return create_dash_app()

# Test layout contains expected component IDs
def test_layout_structure(app):
    layout = app.layout

    def collect_ids(component):
        ids = []
        if hasattr(component, "id") and component.id:
            ids.append(component.id)
        if hasattr(component, "children"):
            children = component.children
            if isinstance(children, list):
                for child in children:
                    ids.extend(collect_ids(child))
            else:
                ids.extend(collect_ids(children))
        return ids

    ids = set(collect_ids(layout))
    expected_ids = {
        "header-h1", "header-h2", "region-selector",
        "date-picker", "submit-button", "output-graph", "error-message"
    }
    for eid in expected_ids:
        assert eid in ids, f"Missing component with id: {eid}"

# Test component types match expected Dash classes
def test_component_types(app):
    layout = app.layout
    expected_types = {
        "header-h1": html.H1,
        "header-h2": html.H2,
        "region-selector": dcc.RadioItems,
        "date-picker": dcc.DatePickerRange,
        "submit-button": html.Button,
        "output-graph": dcc.Graph,
        "error-message": html.Div
    }

    def find_component_by_id(component, target_id):
        if hasattr(component, "id") and component.id == target_id:
            return component
        if hasattr(component, "children"):
            children = component.children
            if isinstance(children, list):
                for child in children:
                    result = find_component_by_id(child, target_id)
                    if result:
                        return result
            else:
                return find_component_by_id(children, target_id)
        return None

    for eid, expected_type in expected_types.items():
        comp = find_component_by_id(layout, eid)
        assert comp is not None, f"Component with id '{eid}' not found"
        assert isinstance(comp, expected_type), f"Component '{eid}' is not of type {expected_type.__name__}"

# Test callback logic with mocked data
def test_callback_logic():
    with patch("new.appfile.task_3.load_data") as mock_load:
        mock_load.return_value = pd.DataFrame({
            "date": ["2023-01-01", "2023-01-02"],
            "region": ["Africa", "Africa"],
            "sales": [100, 150]
        })
        fig = update_graphs("Africa", "2023-01-01", "2023-12-31")
        assert fig is not None
        assert hasattr(fig, "data")
        assert len(fig.data) > 0