import importlib


PygalService = importlib.import_module('services.pygal_service').PygalService


def test_create_xy_chart_with_dict(monkeypatch):
  chart_uri = PygalService.create_xy_chart({'series': [(1, 2), (2, 3)]}, title='dict')

  assert 'series=1' in chart_uri
  assert 'title=dict' in chart_uri


def test_create_xy_chart_with_list():
  chart_uri = PygalService.create_xy_chart([('A', [(1, 2)]), ('B', [(2, 4)])], title='list')

  assert 'series=2' in chart_uri
  assert 'title=list' in chart_uri
