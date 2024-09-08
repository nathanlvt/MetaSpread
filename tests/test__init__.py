import pytest
from metaspread import __init__

def test_imports():
    assert __init__.CancerCell is not None
    assert __init__.CancerModel is not None
    assert __init__.Vessel is not None

def test_check_if_configs_are_present(mocker):
    mocker.patch('metaspread.__init__.check_if_configs_are_present')
    __init__.check_if_configs_are_present()
    assert __init__.check_if_configs_are_present.called

def test_init_simulation_configs(mocker):
    mocker.patch('metaspread.__init__.init_simulation_configs')
    __init__.init_simulation_configs()
    assert __init__.init_simulation_configs.called