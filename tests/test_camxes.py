from camxes import call_camxes, call_vlatai, selmaho
from textwrap import dedent

def camxes_assert_equal(text, arguments, result):
    res = call_camxes(text, arguments) 
    assert res == result,\
        dedent("""called camxes with %r, text %r.
        expected result: %r
        got instead:     %r""") % (arguments, text, result, res)

def test_camxes_text():
    camxes_assert_equal("cipra ui sai", "-t", "cipra ui sai")
    camxes_assert_equal("oi fliba cu fliba", "-t", "oi fliba")
    camxes_assert_equal("hooah!", "-t", "")

def test_camxes_tree():
    assert "cipra" in call_camxes("cipra")
    assert "gerku" in call_camxes("lo gerku cu klama")

def test_camxes_terml():
    assert "cipra" in call_camxes("cipra", "-e")
    assert "gerku" in call_camxes("lo gerku cu klama", "-e")

def test_vlatai():
    assert call_vlatai("jbopre") == ["jbopre", "lujvo", "jbopre"]
    assert call_vlatai("gerku") == ["gerku", "gismu", "gerku"]
    assert call_vlatai("hello") == ["hello", "UNMATCHED", "hello"]

def test_makfa():
    assert selmaho("u'i")[1] == ["UI1"]
    assert selmaho("coi")[1] == ['COI', 'DOhU']
