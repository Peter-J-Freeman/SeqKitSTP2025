import pytest
from SeqToolkit.modules import sequence_manipulation

@pytest.fixture
def seq_tools():
    """Fixture to provide a fresh SequenceTools object for each test."""
    return sequence_manipulation.SequenceTools()


def test_is_dna_valid(seq_tools):
    """Test that valid DNA sequences pass validation."""
    assert seq_tools.is_dna("GATC") is True
    assert seq_tools.is_dna("GATTACA") is True

def test_is_dna_invalid(seq_tools):
    """Test that invalid DNA sequences raise SequenceError."""
    with pytest.raises(sequence_manipulation.SequenceError):
        seq_tools.is_dna("GATX")  # X is invalid
    with pytest.raises(sequence_manipulation.SequenceError):
        seq_tools.is_dna("gatc")  # lower case not allowed

def test_is_rna_valid(seq_tools):
    """Test that valid RNA sequences pass validation."""
    assert seq_tools.is_rna("gauc") is True
    assert seq_tools.is_rna("gauccg") is True

def test_is_rna_invalid(seq_tools):
    """Test that invalid RNA sequences raise SequenceError."""
    with pytest.raises(sequence_manipulation.SequenceError):
        seq_tools.is_rna("gaux")
    with pytest.raises(sequence_manipulation.SequenceError):
        seq_tools.is_rna("GAUC")  # upper case not allowed

def test_reverse_and_attributes(seq_tools):
    """Test reverse method and attribute storage."""
    dna = "GATTACA"
    rev = seq_tools.reverse(dna)
    assert rev == "ACATTAG"
    assert seq_tools.reverse_seq == "ACATTAG"

def test_complement_and_attributes(seq_tools):
    """Test complement method and attribute storage."""
    dna = "GATTACA"
    comp = seq_tools.complement(dna)
    assert comp == "CTAATGT"
    assert seq_tools.complement_seq == "CTAATGT"

def test_reverse_complement_and_attributes(seq_tools):
    """Test reverse_complement method and attribute storage."""
    dna = "GATTACA"
    rev_comp = seq_tools.reverse_complement(dna)
    assert rev_comp == "TGTAATC"
    assert seq_tools.rev_complement_seq == "TGTAATC"

def test_transcribe_and_attributes(seq_tools):
    """Test transcription to RNA and attribute storage."""
    dna = "GATTACA"
    rna = seq_tools.transcribe(dna)
    assert rna == "gauuaca"
    assert seq_tools.rna_sequence == "gauuaca"

def test_translate_and_attributes(seq_tools):
    """Test translation from RNA to protein and attribute storage."""
    rna = "auggaaacu"  # AUG GAA ACU => M E T
    protein = seq_tools.translate(rna)
    assert protein == "MET"
    assert seq_tools.protein_sequence == "MET"

def test_partial_codon_translation(seq_tools):
    """Test that incomplete codons at end are ignored."""
    rna = "augga"  # Only AUG complete, GA incomplete
    protein = seq_tools.translate(rna)
    assert protein == "M"
    assert seq_tools.protein_sequence == "M"
