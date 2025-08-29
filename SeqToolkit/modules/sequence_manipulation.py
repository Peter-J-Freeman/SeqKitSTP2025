"""
Module containing SequenceTools class for manipulation of DNA and RNA sequences.
Provides methods for validation, reverse/complement operations, transcription,
translation, and GenBank-style formatting.
"""
from SeqToolkit.logger import logger
from SeqToolkit.modules.genbank_style import create_genbank_style


class SequenceError(Exception):
    """Exception raised for invalid DNA or RNA sequences."""
    pass


class SequenceTools:
    """
    A class for DNA and RNA sequence manipulation.

    Attributes
    ----------
    dna_alphabet : str
        Allowed DNA bases (uppercase).
    rna_alphabet : str
        Allowed RNA bases (lowercase).
    base_complement : dict
        Complement mapping for DNA bases.
    translation_codes : dict
        RNA codon to amino acid translation table.
    dna_sequence : str
        Last DNA sequence processed.
    rna_sequence : str
        Last RNA sequence processed.
    protein_sequence : str
        Last protein sequence translated from RNA.
    reverse_seq : str
        Last reverse DNA sequence computed.
    complement_seq : str
        Last complement DNA sequence computed.
    rev_complement_seq : str
        Last reverse complement DNA sequence computed.
    """

    def __init__(self):
        """Initialize SequenceTools with DNA/RNA alphabets, codon table, and storage attributes."""
        self.translation_codes = {
            "uuu": "F", "uuc": "F",
            "uua": "L", "uug": "L", "cuu": "L", "cuc": "L", "cua": "L", "cug": "L",
            "ucu": "S", "ucc": "S", "uca": "S", "ucg": "S", "agu": "S", "agc": "S",
            "uau": "Y", "uac": "Y",
            "uaa": "*", "uag": "*", "uga": "*",
            "ugu": "C", "ugc": "C",
            "ugg": "W",
            "ccu": "P", "ccc": "P", "cca": "P", "ccg": "P",
            "cau": "H", "cac": "H",
            "caa": "Q", "cag": "Q",
            "cgu": "R", "cgc": "R", "cga": "R", "cgg": "R", "aga": "R", "agg": "R",
            "auu": "I", "auc": "I", "aua": "I",
            "aug": "M",
            "acu": "T", "acc": "T", "aca": "T", "acg": "T",
            "aau": "N", "aac": "N",
            "aaa": "K", "aag": "K",
            "gau": "D", "gac": "D",
            "gaa": "E", "gag": "E",
            "guu": "V", "guc": "V", "gua": "V", "gug": "V",
            "gcu": "A", "gcc": "A", "gca": "A", "gcg": "A",
            "ggu": "G", "ggc": "G", "gga": "G", "ggg": "G"
        }

        self.base_complement = {"G": "C", "T": "A", "A": "T", "C": "G"}
        self.dna_alphabet = "GATC"
        self.rna_alphabet = "gauc"

        # Attributes for storing the last computed sequences
        self.dna_sequence = None
        self.rna_sequence = None
        self.protein_sequence = None
        self.reverse_seq = None
        self.complement_seq = None
        self.rev_complement_seq = None

    def is_dna(self, dna_sequence):
        """
        Validate that a sequence contains only canonical DNA bases (A, T, G, C).

        Parameters
        ----------
        dna_sequence : str
            DNA sequence to validate (uppercase).

        Returns
        -------
        bool
            True if sequence is valid DNA.

        Raises
        ------
        SequenceError
            If sequence contains invalid characters or is not uppercase.
        """
        if not dna_sequence.isupper():
            raise SequenceError("DNA sequences should be uppercase according to IUPAC standards.")
        for pos, base in enumerate(dna_sequence, start=1):
            if base not in self.dna_alphabet:
                raise SequenceError(f"Non-DNA base {base} at position {pos}")
        logger.info("DNA sequence validation successful.")
        return True

    def is_rna(self, rna_sequence):
        """
        Validate that a sequence contains only canonical RNA bases (a, u, g, c).

        Parameters
        ----------
        rna_sequence : str
            RNA sequence to validate (lowercase).

        Returns
        -------
        bool
            True if sequence is valid RNA.

        Raises
        ------
        SequenceError
            If sequence contains invalid characters or is not lowercase.
        """
        if not rna_sequence.islower():
            raise SequenceError("RNA sequences should be lowercase according to IUPAC standards.")
        for pos, base in enumerate(rna_sequence, start=1):
            if base not in self.rna_alphabet:
                raise SequenceError(f"Non-RNA base {base} at position {pos}")
        logger.info("RNA sequence validation successful.")
        return True

    def reverse(self, dna_sequence):
        """
        Compute the reverse of a DNA sequence.

        Parameters
        ----------
        dna_sequence : str
            DNA sequence to reverse.

        Returns
        -------
        str
            Reversed DNA sequence.
        """
        self.is_dna(dna_sequence)
        self.reverse_seq = dna_sequence[::-1]
        logger.info(f"Reverse sequence: {self.reverse_seq}")
        return self.reverse_seq

    def complement(self, dna_sequence):
        """
        Compute the complement of a DNA sequence.

        Parameters
        ----------
        dna_sequence : str
            DNA sequence to complement.

        Returns
        -------
        str
            Complement DNA sequence.
        """
        self.is_dna(dna_sequence)
        self.complement_seq = "".join([self.base_complement[base] for base in dna_sequence])
        logger.info(f"Complement sequence: {self.complement_seq}")
        return self.complement_seq

    def reverse_complement(self, dna_sequence):
        """
        Compute the reverse complement of a DNA sequence.

        Parameters
        ----------
        dna_sequence : str
            DNA sequence to reverse complement.

        Returns
        -------
        str
            Reverse complement DNA sequence.
        """
        self.is_dna(dna_sequence)
        reverse_bases = self.reverse(dna_sequence)
        self.rev_complement_seq = self.complement(reverse_bases)
        logger.info(f"Reverse complement sequence: {self.rev_complement_seq}")
        return self.rev_complement_seq

    def transcribe(self, dna_sequence, start_position=1):
        """
        Transcribe a DNA sequence to RNA.

        Parameters
        ----------
        dna_sequence : str
            DNA sequence to transcribe.
        start_position : int, optional
            Start position for transcription (1-based, default=1).

        Returns
        -------
        str
            Transcribed RNA sequence.

        Notes
        -----
        Converts thymine (T) to uracil (U) and enforces lowercase RNA alphabet.
        """
        dna_sequence = "".join(dna_sequence.split())
        logger.info(f"Transcribing DNA from position {start_position}: {dna_sequence}")
        self.is_dna(dna_sequence)

        transcribe_this = dna_sequence[start_position - 1:]
        self.rna_sequence = transcribe_this.replace("T", "U").lower()
        self.is_rna(self.rna_sequence)
        logger.info(f"Transcribed RNA: {self.rna_sequence}")
        return self.rna_sequence

    def translate(self, rna_sequence, start_position=1):
        """
        Translate an RNA sequence into a protein sequence.

        Parameters
        ----------
        rna_sequence : str
            RNA sequence to translate.
        start_position : int, optional
            Start position for translation (1-based, default=1).

        Returns
        -------
        str
            Protein sequence (single-letter amino acid codes).

        Notes
        -----
        Translation stops at the first stop codon (*) encountered.
        """
        rna_sequence = "".join(rna_sequence.split())
        logger.info(f"Translating RNA from position {start_position}: {rna_sequence}")
        self.is_rna(rna_sequence)

        translate_this = rna_sequence[start_position - 1:]
        codons = [translate_this[i:i + 3] for i in range(0, len(translate_this), 3)]

        protein = ""
        for codon in codons:
            if len(codon) == 3:
                aa = self.translation_codes[codon]
                protein += aa
                if aa == "*":
                    logger.info(f"Stop codon reached at codon {codon}")
                    protein += aa
                    break
            else:
                logger.warning(f"Incomplete codon {codon} skipped.")

        self.protein_sequence = protein
        logger.info(f"Translated protein: {self.protein_sequence}")
        return self.protein_sequence

    def format_output(self, sequence, chunk_by=10, num_blocks=6):
        """
        Format a nucleotide sequence in GenBank style.

        Parameters
        ----------
        sequence : str
            Sequence to format.
        chunk_by : int, optional
            Number of bases per chunk (default=10).
        num_blocks : int, optional
            Number of chunks per line (default=6).

        Returns
        -------
        str
            GenBank-style formatted sequence.
        """
        from SeqToolkit.modules.chunk_text import chunk_string_to_blocks
        chunk_list = chunk_string_to_blocks(sequence, chunk_by, num_blocks)
        formatted_sequence = create_genbank_style(chunk_list)
        logger.info("Sequence formatted in GenBank style.")
        return formatted_sequence
