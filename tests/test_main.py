import pytest
from metaspread import __main__

def test_imports():
    assert __main__.simrunner is not None
    assert __main__.datagenerator is not None
    assert __main__.graphgenerator is not None
    assert __main__.videogenerator is not None