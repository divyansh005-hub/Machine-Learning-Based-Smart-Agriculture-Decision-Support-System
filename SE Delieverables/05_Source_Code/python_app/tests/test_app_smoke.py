"""Smoke test for Streamlit application imports and page modules."""

import pytest
import importlib


def test_app_and_ui_modules_importable():
    modules = [
        "app",
        "src.ui.styles",
        "src.ui.home_page",
        "src.ui.crop_page",
        "src.ui.fertilizer_page",
        "src.ui.yield_page",
        "src.ui.performance_page",
        "src.ui.insights_page",
        "src.ui.about_page",
    ]
    for mod_name in modules:
        mod = importlib.import_module(mod_name)
        assert mod is not None
