import pytest
from main import BooksCollector

class TestBooksCollector:

    def setup_method(self):
        self.collector = BooksCollector()

    def test_add_new_book(self):
        self.collector.add_new_book('Преступление и наказание')
        assert 'Преступление и наказание' in self.collector.get_books_genre()

    def test_add_new_book_duplicate(self):
        self.collector.add_new_book('Преступление и наказание')
        self.collector.add_new_book('Преступление и наказание')
        assert len(self.collector.get_books_genre()) == 1

    @pytest.mark.parametrize("invalid_name", ["", "a" * 41])
    def test_add_new_book_invalid_name(self, invalid_name):
        self.collector.add_new_book(invalid_name)
        assert invalid_name not in self.collector.get_books_genre()

    def test_set_book_genre(self):
        self.collector.add_new_book('Преступление и наказание')
        self.collector.set_book_genre('Преступление и наказание', 'Детективы')
        assert self.collector.get_book_genre('Преступление и наказание') == 'Детективы'

    @pytest.mark.parametrize("genre,expected", [
        ('Детективы', ['Преступление и наказание']),
        ('Фантастика', []),
    ])
    def test_get_books_with_specific_genre(self, genre, expected):
        self.collector.add_new_book('Преступление и наказание')
        self.collector.set_book_genre('Преступление и наказание', 'Детективы')
        books = self.collector.get_books_with_specific_genre(genre)
        assert books == expected

    def test_get_books_for_children(self):
        self.collector.add_new_book('Преступление и наказание')
        self.collector.set_book_genre('Преступление и наказание', 'Детективы')
        self.collector.add_new_book('Хоббит')
        self.collector.set_book_genre('Хоббит', 'Фантастика')
        books_for_children = self.collector.get_books_for_children()
        assert 'Хоббит' in books_for_children
        assert 'Преступление и наказание' not in books_for_children

    def test_add_book_in_favorites(self):
        self.collector.add_new_book('Хоббит')
        self.collector.add_book_in_favorites('Хоббит')
        assert 'Хоббит' in self.collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate(self):
        self.collector.add_new_book('Хоббит')
        self.collector.add_book_in_favorites('Хоббит')
        self.collector.add_book_in_favorites('Хоббит')
        assert self.collector.get_list_of_favorites_books().count('Хоббит') == 1

    def test_delete_book_from_favorites(self):
        self.collector.add_new_book('Хоббит')
        self.collector.add_book_in_favorites('Хоббит')
        self.collector.delete_book_from_favorites('Хоббит')
        assert 'Хоббит' not in self.collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books(self):
        assert self.collector.get_list_of_favorites_books() == []
        self.collector.add_new_book('Преступление и наказание')
        self.collector.add_book_in_favorites('Преступление и наказание')
        assert self.collector.get_list_of_favorites_books() == ['Преступление и наказание']

    def test_add_new_book_long_name(self):
        long_name = 'Странная история доктора Джекила и мистера Хайда'
        self.collector.add_new_book(long_name)
        assert long_name not in self.collector.get_books_genre()
