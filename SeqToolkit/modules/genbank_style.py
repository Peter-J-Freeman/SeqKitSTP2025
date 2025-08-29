# Import modules
from SeqToolkit.logger import logger

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
