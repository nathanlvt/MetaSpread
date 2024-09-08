import pytest
from metaspread import interactive

def test_main_menu(mocker):
    mocker.patch('metaspread.interactive.main_menu')
    interactive.main_menu()
    assert interactive.main_menu.called