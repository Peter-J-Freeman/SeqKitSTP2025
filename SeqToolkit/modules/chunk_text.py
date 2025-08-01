# Import modules
from SeqToolkit.logger import logger


def chunk_string(query_sequence, chunk_by):
    """
    Split a DNA sequence into evenly sized chunks.

    Parameters:
    query_sequence (str): The DNA sequence string to be split.
    chunk_by (int): The length of each chunk.

    Returns:
    list: A list of fixed-length chunks.
    """
    logger.info("Chunking sequence '{}' into blocks of {}".format(query_sequence, chunk_by))

    my_list = []
    logger.debug("This is a critical print statement which I can switch off by increasing the log level")

    try:
        while query_sequence:
            my_list.append(query_sequence[:chunk_by])
            query_sequence = query_sequence[chunk_by:]
    except TypeError as e:
        logger.error("Chunking failed with exception: {}".format(e))
        raise

    return my_list


def chunk_string_to_blocks(query_sequence, chunk_by, num_blocks, return_lowercase=True):
    """
    Formats a DNA sequence into a list of chunked sequences:
    Each line contains `num_blocks` blocks of length `chunk_by`, with a counter at the start.

    Parameters:
    query_sequence (str): The DNA sequence to be formatted.
    chunk_by (int): The length of each chunk/block.
    num_blocks (int): Number of blocks per line.
    return_lowercase (bool): If True, converts the sequence to lowercase.

    Returns:
    list: A list of rows, where each row is a list of blocks.
    """
    logger.info("Chunking sequence into rows of {} blocks of {}".format(num_blocks, chunk_by))

    if not isinstance(chunk_by, int) or not isinstance(num_blocks, int):
        raise TypeError(f"chunk_by {chunk_by} and num_blocks {num_blocks} must be integers.")

    try:
        # Remove whitespace and optionally convert to lowercase
        query_sequence = "".join(query_sequence.split())
        if return_lowercase:
            query_sequence = query_sequence.lower()

        # Step 1: Use chunk_string() to split into flat list of chunks
        flat_chunks = chunk_string(query_sequence, chunk_by)

        # Step 2: Group the chunks into rows of `num_blocks` blocks each
        # For example, with num_blocks=3: ['aaa', 'bbb', 'ccc', 'ddd'] -> [['aaa', 'bbb', 'ccc'], ['ddd']]
        full_list = [flat_chunks[i:i + num_blocks] for i in range(0, len(flat_chunks), num_blocks)]

    except TypeError as e:
        logger.error("Chunking to blocks failed with exception: {}".format(e))
        raise

    return full_list


# Run this block if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    # Example DNA sequence
    string = "aggagtaagcccttgcaactggaaatacacccattg"
    chunk_length = 5  # Desired chunk length
    print(" ".join(chunk_string(string, chunk_length)))

    # Multiline DNA string (e.g., from FASTA or GenBank)
    string2 = """\
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

    chunk_length = 10   # Length of each chunk
    block_length = 6    # Number of chunks per line

    chunk_list = chunk_string_to_blocks(string2, chunk_length, block_length)
    print(chunk_list)
