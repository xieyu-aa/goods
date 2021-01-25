from django.db import models


# 区域模型类
class Area(models.Model):
    name = models.CharField(verbose_name='名称',max_length=20)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,verbose_name='父类区域',null=True,blank=True)
    class Meta:
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
