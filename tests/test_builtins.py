from validoot.builtins import (
    _,
    numeric,
    text,
    positive,
    negative,
    email_address,
    ip_address,
    url
)

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

def test_positive():
    assert positive(1)
    assert positive(0)
    assert not positive(-1)

def test_negative():
    assert negative(-1)
    assert not negative(0)
    assert not negative(1)

def test_email_address():
    assert email_address('test@mail.com')
    assert email_address('test+test_test@mail.co.za')
    assert not email_address('@mail.co.za')
    assert not email_address('mail.co.za')
    assert not email_address('test@test')

def test_ip_address():
    assert ip_address('172.16.254.1')
    assert ip_address('1.2.3.4')
    assert ip_address('01.102.103.104')
    assert not ip_address('17216.254.1')
    assert not ip_address('1.2.3.4.5')
    assert not ip_address('01 .102.103.104')

def test_url():
    assert url('https://github.com')
    assert url('http://thing.github.com')
    assert url('www.thing.github.com/subfolder/thing?key=value&key2=value2')
    assert not url('http://foo.bar/foo(bar)baz quux')
