import importlib


module = importlib.import_module('services.update_data_service')


def test_extract_x_converts_numeric_columns():
  item = {'id': 1, 'x': '1.5', 'y': '2.5', 'target': '3.5'}

  result = module.extract_x(item)

  assert result == [1.5, 2.5]


def test_extract_y_returns_last_column():
  item = {'id': 1, 'feature': '2.0', 'target': '7.0'}

  result = module.extract_y(item)

  assert result == [7.0]


def test_update_yield_strength_data_uses_helpers(monkeypatch, tmp_path):
  written = {}

  monkeypatch.setattr(module, 'compose_data_for_chart', lambda: {'data1': [(1, 2)]})
  monkeypatch.setattr(module, 'write_data_to_file', lambda data, filename: written.update({'data': data, 'filename': filename}))

  module.UpdateGraphDataService.update_yield_strength_data()

  assert written['filename'] == 'chartData.txt'
  assert written['data'] == {'data1': [(1, 2)]}
