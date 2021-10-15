import csv

from django.apps import apps
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, User, Title, Review


def parse_simple(model_name, path):
    print(f'parse {path}')
    _model = apps.get_model('reviews', model_name)
    with open(path, 'r') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        header = next(rows)
        _model.objects.all().delete()

        for row in rows:
            _object_dict = {key: value for key, value in zip(header, row)}
            _model.objects.get_or_create(**_object_dict)


def parse_title(model_name, path):
    print(f'parse {path}')
    _model = apps.get_model('reviews', model_name)
    with open(path, 'r') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        header = next(rows)
        _model.objects.all().delete()

        for row in rows:
            print(row)
            category = Category.objects.get(pk=int(row[3]))
            _model.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category
            )


def parse_review(model_name, path):
    print(f'parse {path}')
    _model = apps.get_model('reviews', model_name)
    with open(path, 'r') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        header = next(rows)
        _model.objects.all().delete()

        for row in rows:
            print(row)
            title = Title.objects.get(pk=int(row[1]))
            user = User.objects.get(pk=int(row[3]))
            _model.objects.get_or_create(
                id=row[0],
                title=title,
                text=row[2],
                author=user,
                score=row[4],
                pub_date=row[5],
            )


def parse_comment(model_name, path):
    print(f'parse {path}')
    _model = apps.get_model('reviews', model_name)
    with open(path, 'r') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        header = next(rows)
        _model.objects.all().delete()

        for row in rows:
            print(row)
            review = Review.objects.get(pk=int(row[1]))
            user = User.objects.get(pk=int(row[3]))
            _model.objects.get_or_create(
                id=row[0],
                review=review,
                text=row[2],
                author=user,
                pub_date=row[4],
            )


def parse_genre_title(model_name, path):
    print(f'parse {path}')
    with open(path, 'r') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        header = next(rows)

        for row in rows:
            print(row)
            title = Title.objects.get(pk=int(row[1]))
            genre = Genre.objects.get(pk=int(row[2]))
            title.genre.add(genre)


import_list = [
    ('Genre', 'static/data/genre.csv', parse_simple),
    ('Category', 'static/data/category.csv', parse_simple),
    ('User', 'static/data/users.csv', parse_simple),
    ('Title', 'static/data/titles.csv', parse_title),
    ('Review', 'static/data/review.csv', parse_review),
    ('Comment', 'static/data/comments.csv', parse_comment),
    (None, 'static/data/genre_title.csv', parse_genre_title),
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for import_item in import_list:
            import_func = import_item[2]
            import_func(import_item[0], import_item[1])
