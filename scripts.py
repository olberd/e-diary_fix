import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

commendation = ['Молодец!',
                'Отлично!',
                'Хорошо!',
                'Гораздо лучше, чем я ожидал!',
                'Ты меня приятно удивил!',
                'Великолепно!',
                'Прекрасно!',
                'Ты меня очень обрадовал!',
                'Именно этого я давно ждал от тебя!',
                'Сказано здорово – просто и ясно!',
                'Ты, как всегда, точен!',
                'Очень хороший ответ!',
                'Талантливо!',
                'Ты сегодня прыгнул выше головы!',
                'Я поражен!',
                'Уже существенно лучше!',
                'Потрясающе!',
                'Замечательно!',
                'Прекрасное начало!',
                'Так держать!',
                'Ты на верном пути!',
                'Здорово!',
                'Это как раз то, что нужно!',
                'Я тобой горжусь!',
                'С каждым разом у тебя получается всё лучше!',
                'Мы с тобой не зря поработали!',
                'Я вижу, как ты стараешься!',
                'Ты растешь над собой!',
                'Ты многое сделал, я это вижу!',
                'Теперь у тебя точно все получится!',
                ]


def get_child(schoolkid):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print('Нет такого ученика')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников')


def fix_marks(schoolkid):
    child = get_child(schoolkid)
    bad_marks = Mark.objects.filter(schoolkid=child.id, points__lte=3)
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    child = get_child(schoolkid)
    child_chastisements = Chastisement.objects.filter(schoolkid=child.id)
    child_chastisements.delete()


def create_commendation(schoolkid, subject):
    random_commendation = random.choice(commendation)
    kid = get_child(schoolkid)
    lessons = Lesson.objects.filter(subject__title=subject, year_of_study=kid.year_of_study,
                                    group_letter=kid.group_letter).order_by('-date')
    if not lessons:
        print(f'Не можем найти такой предмет: {subject}')
        return
    random_lesson = random.choice(lessons)
    Commendation.objects.create(text=random_commendation, created=random_lesson.date, schoolkid=kid,
                                subject=random_lesson.subject, teacher=random_lesson.teacher)
