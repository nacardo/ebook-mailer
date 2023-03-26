import os
import sys

import pytest

sys.path.append(r"/home/nick/Documents/Dev/Projects/ebook_processor/src")
from book import Book


# print(os.listdir("."))


@pytest.fixture()
def create_book():
    return Book('Flowers_for_Algernon_by_Daniel_Keyes.epub')


def test_get_title(create_book):
    book = create_book
    assert book.get_title() == 'Flowers for Algernon'


def test_get_author(create_book):
    book = create_book
    assert book.get_author() == 'Daniel Keyes'
