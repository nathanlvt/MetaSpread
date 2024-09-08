import pytest
from metaspread import cancermodel

def test_imports():
    assert cancermodel.mesa is not None
    assert cancermodel.plt is not None
    assert cancermodel.np is not None
    assert cancermodel.pd is not None
    assert cancermodel.os is not None
    assert cancermodel.json is not None
    assert cancermodel.ast is not None
    assert cancermodel.CancerCell is not None
    assert cancermodel.Vessel is not None
    assert cancermodel.find_quasi_circle is not None

def test_generate_cancer_model(mocker):
    mocker.patch('metaspread.cancermodel.generate_cancer_model')
    cancermodel.generate_cancer_model()
    assert cancermodel.generate_cancer_model.called