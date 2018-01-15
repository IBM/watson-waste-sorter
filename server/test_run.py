import run


def test_run():
    assert run.default() == ''


def test_sort():
    assert run.sort() != ''
