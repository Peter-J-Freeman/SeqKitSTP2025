# Import modules
from SeqToolkit.loger import logger

def create_genbank_style(chunk_list):
    counter = 0       # Keeps track of total base count, used for the GenBank-style line prefix
    text_out = ""     # Final formatted output string

    try:
        for line in chunk_list:
            counter += 1  # Line prefix is 1-based index of first base, mimicking GenBank format
            row = " ".join(line)  # Join blocks with spaces
            text_out += "{}\t{}{}".format(str(counter), row, "\n")

            # Update the counter to reflect total bases seen so far
            # (row.split() removes whitespace; ''.join(...) gives total base count in this line)
            counter += len("".join(row.split())) - 1
    except TypeError as e:
        logger.error(f"create_genbank_style failed with error: {e}")

    return text_out


# Example usage if script is run directly
if __name__ == "__main__":
    from SeqToolkit.modules.chunk_text import chunk_string_to_blocks

    # Multiline string simulating a DNA sequence input (could be from FASTA or GenBank)
    string = """\
    GCTGAGACTTCCTGGACGGGGGACAGGCTGTGGGGTTTCTCAGATAACTGGGCCCCTGCGCTCAGGAGGC
    CTTCACCCTCTGCTCTGGGTAAAGTTCATTGGAACAGAAAGAAATGGATTTATCTGCTCTTCGCGTTGAA
    GAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGG
    AACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAATTTTGCATGCTGAAACTTCTCAACCAGAAGAA
    AGGGCCTTCACAGTGTCCTTTATGTAAGAATGATATAACCAAAAGGAGCCTACAAGAAAGTACGAGATTT
    AGTCAACTTGTTGAAGAGCTATTGAAAATCATTTGTGCTTTTCAGCTTGACACAGGTTTGGAGTATGCAA
    ACAGCTATAATTTTGCAAAAAAGGAAAATAACTCTCCTGAACATCTAAAAGATGAAGTTTCTATCATCCA
    AAGTATGGGCTACAGAAACCGTGCCAAAAGACTTCTACAGAGTGAACCCGAAAATCCTTCCTTGCAGGAA
    ACCAGTCTCAGTGTCCAACTCTCTAACCTTGGAACTGTGAGAACTCTGAGGACAAAGCAGCGGATACAAC
    CTCAAAAGACGTCTGTCTACATTGAATTGGGATCTGATTCTTCTGAAGATACCGTTAATAAGGCAACTTA
    TTGCAGTGTGGGAGATCAAGTAAATAAAAAAAAAAAA"""

    chunk_length = 10   # Length of each chunk (e.g., block of 10 bases)
    block_length = 6    # Number of blocks per line (e.g., 6 blocks of 10 bases = 60 bases per line)

    # Print the formatted sequence
    chunk_list = (chunk_string_to_blocks(string, chunk_length, block_length))
    print(create_genbank_style(chunk_list))
