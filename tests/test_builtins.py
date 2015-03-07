from validoot.builtins import _, numeric, text

def test_underscore():
    assert _(None)
    assert not _(1)
    assert not _([])

def test_numeric():
    assert numeric(1)
    assert numeric(1.0)
    assert not numeric('string')

def test_text():
    assert text('string')
    assert text(u'unicode')
    assert not text(1)
