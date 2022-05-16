from page_loader.page_loader import main


def test_cli_interface(capsys):
    main(['https://python-poetry.org/docs/', "--output", "$HOME/page-loader/"])
    captured = capsys.readouterr()
    assert captured.out == "$HOME/page-loader/python-poetry-org-docs.html\n"
    main(['https://python-poetry.org/docs/', "--output", "$HOME/page-loader/"])
    captured = capsys.readouterr()
    assert captured.out == "$HOME/page-loader/python-poetry-org-docs.html\n"
