import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypesChoices(models.TextChoices):
        MOVIE = "movie"
        TV_SHOW = "tv_show"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_path = models.FileField(_('file'),
                                 blank=True, null=True,
                                 upload_to='admin_movies_files/')
    title = models.CharField(_('title'), max_length=255, null=False)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    description = models.TextField('description', blank=True)
    creation_date = models.DateTimeField('creation_date')
    rating = models.FloatField('rating', blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField('type', choices=TypesChoices.choices)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [models.Index(fields=['film_Work', 'genre'])]


class Person(UUIDMixin, TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.TextField('full_name', null=False)


class PersonFilmwork(UUIDMixin):
    class Roles(models.TextChoices):
        ACTOR = 'actor'
        PRODUCER = 'producer'
        DIRECTOR = 'director'

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', choices=Roles.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['film_Work', 'person'])]
