from page_loader.page_loader import main


def test_download():
    pass


def test_main(capsys):
    main(['https://python-poetry.org/docs/', "--output", "tmp/home/"])
    captured = capsys.readouterr()
    assert captured.out == "tmp/home/python-poetry-org-docs.html\n"
    main(['https://python-poetry.org/docs/', "--output", "/tmp/home/"])
    captured = capsys.readouterr()
    assert captured.out == "/tmp/home/python-poetry-org-docs.html\n"
    # with open('fixtures/courses_fake.html') as page:
