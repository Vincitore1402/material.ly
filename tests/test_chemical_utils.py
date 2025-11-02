import importlib
import math


module = importlib.import_module('utils.chemical_utils')


def test_simple_compare_returns_zero_for_identical_data():
  base = [
    {'atomic_Number': 6, 'average': 0.5},
    {'atomic_Number': 8, 'average': 0.2}
  ]

  result = module.simple_compare(base, list(base))

  assert result == 0


def test_simple_compare_computes_euclidean_distance():
  first = [
    {'atomic_Number': 6, 'average': 0.5},
    {'atomic_Number': 8, 'average': 0.1}
  ]
  second = [
    {'atomic_Number': 6, 'average': 0.2},
    {'atomic_Number': 10, 'average': 0.3}
  ]

  result = module.simple_compare(first, second)

  expected = math.sqrt((0.5 - 0.2) ** 2 + 0.1 ** 2 + 0.3 ** 2)
  assert math.isclose(result, expected)


def test_get_chemical_composition_filters_by_material():
  dataset = [
    {'main_info_id': 1, 'value': 'a'},
    {'main_info_id': 2, 'value': 'b'},
    {'main_info_id': 1, 'value': 'c'}
  ]

  result = module.get_chemical_composition(1, dataset)

  assert result == [
    {'main_info_id': 1, 'value': 'a'},
    {'main_info_id': 1, 'value': 'c'}
  ]
