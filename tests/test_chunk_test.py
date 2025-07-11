import pytest
from SeqToolkit.modules import chunk_text


# ------------------------------
# Tests for chunk_string()
# ------------------------------

def test_chunk_string_regular_case():
    seq = "aggagtaagcccttgcaactggaaatacacccattg"
    expected = ['aggag', 'taagc', 'ccttg', 'caact', 'ggaaa', 'tacac', 'ccatt', 'g']
    assert chunk_text.chunk_string(seq, 5) == expected

def test_chunk_string_chunk_size_as_string():
    seq = "aggagtaagcccttgcaactggaaatacacccattg"
    with pytest.raises(TypeError):
        chunk_text.chunk_string(seq, "5")

def test_chunk_string_empty_sequence():
    assert chunk_text.chunk_string("", 5) == []

def test_chunk_string_chunk_larger_than_sequence():
    assert chunk_text.chunk_string("agg", 10) == ["agg"]


# ------------------------------
# Tests for chunk_string_to_blocks()
# ------------------------------

def test_chunk_string_to_blocks_regular_input():
    seq = "ACTGGTAGTCAGTCAAGTCA"
    result = chunk_text.chunk_string_to_blocks(seq, 5, 2)
    assert result == [['actgg', 'tagtc'], ['agtca', 'agtca']]

def test_chunk_string_to_blocks_partial_final_row():
    seq = "AAAGGGCCCTTT"  # 12 bases
    result = chunk_text.chunk_string_to_blocks(seq, 4, 2)
    assert result == [['aaag', 'ggcc'], ['cttt']]

def test_chunk_string_to_blocks_exact_fit():
    seq = "AAAAGGGGCCCC"  # 12 bases
    result = chunk_text.chunk_string_to_blocks(seq, 4, 3)
    assert result == [['aaaa', 'gggg', 'cccc']]

def test_chunk_string_to_blocks_multi_line_input():
    seq = """AAAAGGGG
             CCCC TTTT
             GGGGAAAA"""
    result = chunk_text.chunk_string_to_blocks(seq, 4, 2)
    assert result == [['aaaa', 'gggg'], ['cccc', 'tttt'], ['gggg', 'aaaa']]

def test_chunk_string_to_blocks_disable_lowercase():
    seq = "AaAaGGgg"
    result = chunk_text.chunk_string_to_blocks(seq, 2, 2, return_lowercase=False)
    assert result == [['Aa', 'Aa'], ['GG', 'gg']]

def test_chunk_string_to_blocks_empty_input():
    assert chunk_text.chunk_string_to_blocks("", 4, 3) == []

def test_chunk_string_to_blocks_chunk_as_string_raises():
    with pytest.raises(TypeError):
        chunk_text.chunk_string_to_blocks("AAGGTT", "2", 2)

def test_chunk_string_to_blocks_num_blocks_as_string_raises():
    with pytest.raises(TypeError):
        chunk_text.chunk_string_to_blocks("AAGGTT", 2, "2")

def test_chunk_string_to_blocks_invalid_chunk_type_raises():
    with pytest.raises(TypeError):
        chunk_text.chunk_string_to_blocks("AAGGTT", "2", 3)

def test_chunk_string_to_blocks_invalid_num_blocks_type_raises():
    with pytest.raises(TypeError):
        chunk_text.chunk_string_to_blocks("AAGGTT", 3, "3")

