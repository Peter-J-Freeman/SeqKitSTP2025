from SeqToolkit.modules import genbank_style


def test_create_genbank_style_typical():
    chunk_list = [
        ['atgc', 'ggta', 'ccta'],  # 4 + 4 + 4 = 12 bases
        ['ttaa', 'ccgg'],          # 4 + 4 = 8 bases
        ['ggcc']                   # 4 bases
    ]
    result = genbank_style.create_genbank_style(chunk_list)
    expected = (
        "1\tatgc ggta ccta\n"    # starts at 1
        "13\tttaa ccgg\n"        # 1 + 12 = 13
        "21\tggcc\n"             # 13 + 8 = 21
    )
    assert result == expected


def test_create_genbank_style_empty():
    assert genbank_style.create_genbank_style([]) == ""


def test_create_genbank_style_single_chunk():
    chunk_list = [['atgc']]
    result = genbank_style.create_genbank_style(chunk_list)
    expected = "1\tatgc\n"
    assert result == expected


def test_create_genbank_style_invalid_input_logs_error(monkeypatch):
    # Patch logger.error to track if it was called
    called = {}

    def fake_error(msg):
        called['msg'] = msg

    monkeypatch.setattr(genbank_style.logger, "error", fake_error)

    # Pass invalid input (e.g. None)
    result = genbank_style.create_genbank_style(None)

    # Function returns empty string on exception
    assert result == ""

    # Logger.error should have been called once with the expected message
    assert 'msg' in called
    assert "failed with error" in called['msg']
