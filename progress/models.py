from django.db import models
from django.contrib.auth.models import User


class Target(models.Model):
    user = models.CharField(max_length= 50, default= "Ellen")
    target_description = models.CharField(max_length=300)
    target = models.SmallIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.SmallIntegerField (default=1, help_text='приоритет в показе')
    done = models.PositiveIntegerField(default=0)

    def _get_current_status(self):
        import datetime
        from datetime import date, datetime
        current_date = date.today()
        task_duration = (self.end_date - self.start_date).days + 1
        target_per_day = self.target / task_duration
        to_be_done = target_per_day * ((current_date - self.start_date).days  + 1) #на сегодня
        if target_per_day == 0:
            return target_per_day
        else:
            diff_days = round(self.done - to_be_done) / target_per_day
            #done_persentage = self.done * 100 / self.target
            #return (self.end_date - self.start_date).days
            return round(diff_days,1)

    def _get_persentage(self):
        if self.target == 0:
            return 0
        else:
            return  int(self.done * 100 / self.target)

    f1 = property(_get_current_status)
    f2 = property(_get_persentage)


    class Meta:
        ordering = ['priority', 'target_description']
