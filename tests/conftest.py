"""Load the external test data and give every row its own pytest ID."""
import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def pytest_generate_tests(metafunc):
    if 'case' not in metafunc.fixturenames:
        return
    function = metafunc.function.__name__.removeprefix('test_')
    with (ROOT / 'data' / 'validation_cases.csv').open(encoding='utf-8', newline='') as f:
        rows = [row for row in csv.DictReader(f) if row['function'] == function]
    if len(rows) != 20 or len({r['id'] for r in rows}) != len(rows):
        raise pytest.UsageError(f'{function}: expected 20 uniquely identified CSV cases')
    params = []
    for row in rows:
        row['value'] = json.loads(row['value_json'])
        row['options'] = json.loads(row['options_json'])
        marks = [getattr(pytest.mark, row['allocation'].lower()),
                 pytest.mark.boundary if row['technique'] == 'BVA' else pytest.mark.ecp]
        if row['smoke'] == 'yes':
            marks.append(pytest.mark.smoke)
        if row['expected'] != 'valid':
            marks.append(pytest.mark.negative)
        params.append(pytest.param(row, id=row['id'], marks=marks))
    metafunc.parametrize('case', params)


@pytest.fixture(autouse=True)
def predictable_raise_mode(monkeypatch):
    monkeypatch.delenv('RAISE_VALIDATION_ERROR', raising=False)


@pytest.fixture
def check_validation():
    from validators import ValidationError

    def check(function, case):
        if case['expected'] == 'raises':
            with pytest.raises(ValidationError) as exc:
                function(case['value'], **case['options'])
            result = exc.value
        else:
            result = function(case['value'], **case['options'])
            if case['expected'] == 'valid':
                assert result is True
                return
            assert isinstance(result, ValidationError)
            assert not result
        assert result.func.__name__ == function.__name__
        assert result.value == case['value']
    return check
