# Import modules
from SeqToolkit.loger import logger

def chunk_string(query_sequence, chuk_by):
    """
    Split a DNA sequence into evenly sized chunks.

    Parameters:
    query_sequence (str): The DNA sequence string to be split.
    chuk_by (int): The length of each chunk.

    Returns:
    str: A string of space-separated chunks.
    """
    logger.info("Chunk {} into blocks of {}".format(query_sequence, str(chuk_by)))

    # Initialize a list to hold each chunk
    my_list = []

    # This is a DEBUG-level message; useful for development or troubleshooting
    logger.debug("This is a critical print statement which I can switch off by increasing the log level")

    # Loop through the sequence, taking slices of length `chuk_by` until empty
    try:
        while query_sequence:
            # Take the first `chuk_by` characters and add to the list
            my_list.append(query_sequence[:chuk_by])
            # Remove those characters from the sequence
            query_sequence = query_sequence[chuk_by:]
    except TypeError as e:
        logger.error("Chunk {} failed with exception: {}".format(query_sequence, e))
        raise

    # Join the chunks with spaces and return the result
    return my_list

def chunk_string_to_blocks(query_sequence, chuk_by, num_blocks, return_lowercase=True):
    """
    Formats a DNA sequence into a list of chunked sequences:
    Each line contains `num_blocks` blocks of length `chuk_by`, with a counter at the start.

    Parameters:
    query_sequence (str): The DNA sequence to be formatted
    chuk_by (int): The length of each chunk/block
    num_blocks (int): Number of blocks per line

    Returns:
    list: A list of lines formatted
    """
    logger.info("Chunking sequence into rows of {} blocks of {}".format(num_blocks, chuk_by))

    if not isinstance(chuk_by, int) or not isinstance(num_blocks, int):
        raise TypeError(f"chuk_by {chuk_by} and num_blocks {num_blocks} must be integers.")

    try:
        # Remove all whitespace and convert sequence to lowercase
        query_sequence = "".join(query_sequence.split())
        if return_lowercase:
            query_sequence = query_sequence.lower()

        full_list = []   # List to hold all rows (each row is a list of blocks)
        inner_list = []  # Temporary list to build a single row

        while query_sequence:
            if len(inner_list) == num_blocks:
                # Current row is full, so add it to the full list and reset
                full_list.append(inner_list)
                inner_list = []
            # Append the next chunk to the current row
            inner_list.append(query_sequence[:chuk_by])
            # Remove the chunk from the sequence
            query_sequence = query_sequence[chuk_by:]

        # Add any remaining blocks in inner_list that didn't make a full row
        if inner_list:
            full_list.append(inner_list)
    except TypeError as e:
        logger.error("Chunk {} failed with exception: {}".format(query_sequence, e))
        raise

    return full_list


# Run this block if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    # Example DNA sequence
    string = "aggagtaagcccttgcaactggaaatacacccattg"
    # Desired chunk length
    chunk_length = 5
    # Output the chunked string
    print(" ".join(chunk_string(string, chunk_length)))

    # Multiline string simulating a DNA sequence input (could be from FASTA or GenBank)
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

    chunk_length = 10   # Length of each chunk (e.g., block of 10 bases)
    block_length = 6    # Number of blocks per line (e.g., 6 blocks of 10 bases = 60 bases per line)

    # Print the formatted sequence
    chunk_list = (chunk_string_to_blocks(string2, chunk_length, block_length))
    print(chunk_list)

