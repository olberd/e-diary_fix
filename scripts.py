import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

COMMENDATION = ['Молодец!',
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


def get_child(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print('Нет такого ученика.')
        raise
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников.')
        raise


def fix_marks(schoolkid_name):
    child = get_child(schoolkid_name)
    Mark.objects.filter(schoolkid=child.id, points__lte=3).update(points=5)


def remove_chastisements(schoolkid_name):
    child = get_child(schoolkid_name)
    child_chastisements = Chastisement.objects.filter(schoolkid=child.id)
    child_chastisements.delete()


def create_commendation(schoolkid_name, subject):
    random_commendation = random.choice(COMMENDATION)
    kid = get_child(schoolkid_name)
    lessons = Lesson.objects.filter(subject__title=subject, year_of_study=kid.year_of_study,
                                    group_letter=kid.group_letter).order_by('-date')
    if not lessons:
        print('Таких уроков по предмету не найдено.')
        return
    random_lesson = random.choice(lessons)
    Commendation.objects.create(text=random_commendation, created=random_lesson.date, schoolkid=kid,
                                subject=random_lesson.subject, teacher=random_lesson.teacher)
