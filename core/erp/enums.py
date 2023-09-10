from django.db.models import TextChoices


class WorkArea(TextChoices):
    LASER = ('LASER', 'Лазерный участок')
    WELDING = ('WELDING', 'Сварочный участок')
    MOTOR = ('MOTOR', 'Моторный участок')
    ELECTRICIAN = ('ELECTRICIAN', 'Участок электрики')
    ASSEMBLY = ('ASSEMBLY', 'Сборочный участок')

    @classmethod
    def get_label_by_name(cls, value):
        for name, label in cls.choices:
            if name == value:
                return label
