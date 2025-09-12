import requests
import xmltodict
from SeqToolkit.logger import logger


class TranscriptIdError(Exception):
    """
    Custom exception raised when a transcript identifier does not meet the
    expected NCBI format requirements.
    """
    pass


def fetch_transcript_record(transcript_id):
    """
    Fetch a transcript record from the NCBI Nucleotide database using the
    Entrez EFetch API, and return the record as a Python dictionary
    (converted from XML).

    Parameters:
    transcript_id (str): A transcript accession with version number.
        Must start with NM_, NR_, XM_, or XR_ (e.g., "NM_000093.4").

    Returns:
    dict: A Python dictionary representation of the transcript record,
        parsed from the XML response.

    Raises:
    TranscriptIdError: If the transcript_id does not have the expected prefix
        or lacks a version number.
    requests.exceptions.RequestException: If there is a network or API error.
    """

    # Validate that the transcript ID has the expected RefSeq prefix
    if not transcript_id.startswith(("NM_", "NR_", "XM_", "XR_")):
        raise TranscriptIdError(
            f"Invalid transcript ID: {transcript_id}. "
            "Must start with NM_, NR_, XM_, or XR_."
        )

    # Validate that the transcript ID includes a version (e.g., ".3")
    if "." not in transcript_id:
        raise TranscriptIdError(
            f"Transcript ID {transcript_id} must include a version number "
            "(e.g., NM_000093.4)."
        )

    # Base URL for NCBI Entrez EFetch
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",   # NCBI nucleotide database
        "id": transcript_id,  # transcript accession
        "retmode": "xml"      # request XML format for easier parsing
    }

    try:
        # Perform GET request to NCBI EFetch
        r = requests.get(url, params=params)
        r.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching transcript {transcript_id}: {e}")
        raise

    # Convert XML response to Python dict using xmltodict and stript out the GBSet/GBSeq wrapper
    return xmltodict.parse(r.text)['GBSet']['GBSeq']


if __name__ == "__main__":
    # Example usage: fetch a GenBank transcript record (e.g. COL5A1 mRNA RefSeq)
    record = fetch_transcript_record("NM_000093.5")

    # Top-level metadata fields from the GenBank record
    print(record['GBSeq_accession-version'])   # Accession with version, e.g. "NM_000093.5"
    print(record['GBSeq_definition'])          # Definition line, e.g. "collagen alpha-1(V) chain (COL5A1), mRNA"
    print(record['GBSeq_keywords'])            # Keywords list, e.g. ["RefSeq", "mRNA", "collagen"]

    # Print the raw nucleotide sequence in uppercase
    print(record['GBSeq_sequence'].upper())

    # Iterate over all annotated features in the feature table
    for line in record['GBSeq_feature-table']['GBFeature']:

        # --- Gene feature ---
        if line['GBFeature_key'] == 'gene':
            # Gene symbol, e.g. "COL5A1"
            print(line['GBFeature_quals']['GBQualifier'][0]['GBQualifier_value'])
            # HGNC ID (sometimes appears as "HGNC:HGNC:2197", so fix formatting)
            print(line['GBFeature_quals']['GBQualifier'][4]['GBQualifier_value']
                  .replace("HGNC:HGNC:", "HGNC:"))

        # --- Coding sequence (CDS) feature ---
        elif line['GBFeature_key'] == 'CDS':
            # Start coordinate of coding region on the transcript
            print(line['GBFeature_intervals']['GBInterval']['GBInterval_from'])
            # End coordinate of coding region on the transcript
            print(line['GBFeature_intervals']['GBInterval']['GBInterval_to'])

    # Keywords again (redundant, but ensures access outside the loop)
    print(record['GBSeq_keywords'])

    # Print all top-level keys in the record dict for exploration/debugging
    print(record.keys())

