import pytest
from metaspread import configs

def test_imports():
    assert configs.pd is not None
    assert configs.os is not None
    assert configs.ast is not None

def test_init_simulation_configs(mocker):
    mocker.patch('metaspread.configs.init_simulation_configs')
    configs.init_simulation_configs('mock_configs.csv')
    assert configs.init_simulation_configs.called