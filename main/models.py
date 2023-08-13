from django.db import models

# Create your models here.

class User_data(models.Model):
    name=models.CharField(max_length=30 ,primary_key=True)
    staff_code=models.IntegerField()
    score=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Ranking(models.Model):
    posted_by=models.CharField(max_length=20)
    name=models.ForeignKey(User_data, verbose_name=("name"), on_delete=models.PROTECT)
    ranking=models.IntegerField()
    score=models.IntegerField()
    reason=models.CharField(max_length=50 ,null=False)
    want_to=models.CharField(max_length=50,null=False)
    Ranking_title=models.ForeignKey("Setting",verbose_name=("順位付けタイトル"),on_delete=models.PROTECT)


class Setting(models.Model):
    Ranking_title=models.CharField(max_length=50,verbose_name="開催名")
    Num_of_people=models.IntegerField(verbose_name="対象人数")
    publicity=models.BooleanField(default=False,verbose_name="名前公開",help_text="回答者氏名を公表する場合はTrue")
    is_open=models.BooleanField(default=False,verbose_name="受付状況",help_text="回答を受け付ける場合はTrue")
    calculated=models.BooleanField(default=False,verbose_name="集計済みか否か")
    def __str__(self):
        return self.Ranking_title

