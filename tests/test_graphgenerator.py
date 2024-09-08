import pytest
from metaspread import graphgenerator

def test_imports():
    assert graphgenerator.ast is not None
    assert graphgenerator.pd is not None
    assert graphgenerator.plt is not None
    assert graphgenerator.np is not None
    assert graphgenerator.re is not None
    assert graphgenerator.os is not None
    assert graphgenerator.sys is not None
    assert graphgenerator.metaspread.configs is not None

def test_generate_graph(mocker):
    mocker.patch('metaspread.graphgenerator.generate_graph')
    graphgenerator.generate_graph()
    assert graphgenerator.generate_graph.called