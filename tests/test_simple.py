import pytest
from buildpg import MultipleValues, Raw, RawDangerous, Values, render


args = 'template', 'ctx', 'expected_query', 'expected_params'
TESTS = [
    {
        'template': 'simple: {{ v }}',
        'ctx': dict(v=1),
        'expected_query': 'simple: $1',
        'expected_params': [1],
    },
    {
        'template': 'multiple: {{ a}} {{c }} {{b}}',
        'ctx': dict(a=1, b=2, c=3),
        'expected_query': 'multiple: $1 $2 $3',
        'expected_params': [1, 3, 2],
    },
    {
        'template': 'values: {{ a }}',
        'ctx': dict(a=Values(1, 2, 3)),
        'expected_query': 'values: ($1, $2, $3)',
        'expected_params': [1, 2, 3],
    },
    {
        'template': 'named values: {{ a }} {{ a.names }}',
        'ctx': dict(a=Values(foo=1, bar=2)),
        'expected_query': 'named values: ($1, $2) foo, bar',
        'expected_params': [1, 2],
    },
    {
        'template': 'multiple values: {{ a }}',
        'ctx': dict(a=MultipleValues(
            Values(3, 2, 1),
            Values('i', 'j', 'k')
        )),
        'expected_query': 'multiple values: ($1, $2, $3), ($4, $5, $6)',
        'expected_params': [3, 2, 1, 'i', 'j', 'k'],
    },
    {
        'template': 'raw: {{the_raw_values}}',
        'ctx': dict(the_raw_values=Raw('x', 'y', 4)),
        'expected_query': 'raw: x, y, 4',
        'expected_params': [],
    },
    {
        'template': 'raw dangerous: {{the_raw_values}}',
        'ctx': dict(the_raw_values=RawDangerous('x', '"y"', 4)),
        'expected_query': 'raw dangerous: x, "y", 4',
        'expected_params': [],
    },
]


@pytest.mark.parametrize(','.join(args), [[t[a] for a in args] for t in TESTS], ids=[t['template'] for t in TESTS])
def test_render(template, ctx, expected_query, expected_params):
    query, params = render(template, **ctx)
    assert query == expected_query
    assert params == expected_params
