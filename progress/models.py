from django.db import models
from django.contrib.auth.models import User


class Target(models.Model):
    user = models.ForeignKey(User)
    target_description = models.CharField(max_length=300)
    target = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.SmallIntegerField (default=1, help_text='приоритет в показе',
                                         choices=((1,'обычный порядок'),
                                                  (0,'показывать в начале'),)
                                         )
    done = models.PositiveIntegerField(default=0)

    def _get_current_status(self):

        from datetime import date, datetime
        current_date = date.today()
        task_duration = (self.end_date - self.start_date).days + 1
        target_per_day = self.target / task_duration
        to_be_done = target_per_day * ((current_date - self.start_date).days  + 1) #на сегодня

        if target_per_day == 0:
            return target_per_day

        diff_days = int((self.done - to_be_done) / target_per_day)

        return diff_days



    def _get_persentage(self):
        if self.target == 0:
            return 0
        else:
            return  int(self.done * 100 / self.target)

    f1 = property(_get_current_status)
    f2 = property(_get_persentage)

    def _wording (self):

        last_digit = int(str(self.f1)[-1])
        if last_digit in [0,5,6,7,8,9]:
            part2 = "дней"
        elif last_digit in [2,3,4]:
            part2 = "дня"
        else:
            part2 = 'день'

        if self.f1 == 0:
            return "В графике".format()
        elif self.f1 > 0:
            return 'Впереди на {} {}'.format(self.f1, part2)
        else:
            return 'Отстаем на {} {}'.format(abs(self.f1), part2)

    word = property(_wording)

    class Meta:
        ordering = ['priority', 'target_description']


