from django.db import models
from django.contrib.auth.models import User


class Target(models.Model):
    user = models.ForeignKey(User)
    target_description = models.CharField(max_length=300,)
    target = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.SmallIntegerField(default=1, help_text='приоритет в показе',
                                        choices=((1, 'обычный порядок'),
                                                 (0, 'показывать в начале'),)
                                        )
    done = models.PositiveIntegerField(default=0)

    def _get_current_status(self):

        from datetime import date, datetime
        current_date = date.today()
        task_duration = (self.end_date - self.start_date).days + 1
        target_per_day = self.target / task_duration
        to_be_done = target_per_day * ((current_date - self.start_date).days + 1)  # на сегодня

        if target_per_day == 0:
            return target_per_day

        diff_days =  (self.done - to_be_done) / target_per_day

        return diff_days

    def _get_persentage(self):
        if self.target == 0:
            return 0
        else:
            result = int(self.done * 100 / self.target)
            if result <= 100:
                return result
            else:
                return 100

    def _wording(self):

        if self.f1 == 0:
            return "В графике".format()
        elif self.f1 > 0:
            #return 'Впереди на {} {}'.format(self.f1, part2)
            return 'Впереди'
        else:
            #return 'Отстаем на {} {}'.format(abs(self.f1), part2)
            return 'Отстаем'

    def _todo_daily(self):
        from datetime import date, datetime
        current_date = date.today()
        task_duration = (self.end_date - self.start_date).days + 1
        target_per_day = self.target / task_duration
        #to_be_done = target_per_day * ((current_date - self.start_date).days + 1)  # на сегодня
        return target_per_day

    def _tobe_done(self):

        from datetime import date, datetime
        current_date = date.today()
        task_duration = (self.end_date - self.start_date).days + 1
        target_per_day = self.target / task_duration
        to_be_done_today = target_per_day * ((current_date - self.start_date).days + 1)  # на сегодня

        if self.target == 0:
            return 0
        else:
            to_be_done_today = to_be_done_today * 100/self.target
            if to_be_done_today >=100:
                return 100
            else:
                return int(to_be_done_today)

    def _left_todo(self):
        if (self.target - self.done) > 0:
            return (self.target - self.done)
        else:
            return 0


    f1 = property(_get_current_status)
    f2 = property(_get_persentage)
    word = property(_wording)
    daily = property(_todo_daily)
    todo_today = property(_tobe_done)
    left_todo = property(_left_todo)

    class Meta:
        ordering = ['priority', 'target_description']
