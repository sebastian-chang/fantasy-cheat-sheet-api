from django.db import models


class QBStats(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    week = models.BigIntegerField(blank=True, null=True)
    season = models.BigIntegerField(blank=True, null=True)
    homeoraway = models.TextField(db_column='HomeOrAway', blank=True, null=True)
    opponent = models.TextField(db_column='Opponent', blank=True, null=True)
    passattempts = models.BigIntegerField(db_column='passAttempts', blank=True, null=True)
    passcompletions = models.BigIntegerField(db_column='passCompletions', blank=True, null=True)
    passpct = models.FloatField(db_column='passPct', blank=True, null=True)
    passyards = models.BigIntegerField(db_column='passYards', blank=True, null=True)
    passavg = models.FloatField(db_column='passAvg', blank=True, null=True)
    passyardsperatt = models.FloatField(db_column='passYardsPerAtt', blank=True, null=True)
    passtd = models.BigIntegerField(db_column='passTD', blank=True, null=True)
    passtdpct = models.FloatField(db_column='passTDPct', blank=True, null=True)
    passint = models.BigIntegerField(db_column='passInt', blank=True, null=True)
    passintpct = models.FloatField(db_column='passIntPct', blank=True, null=True)
    passlng = models.BigIntegerField(db_column='passLng', blank=True, null=True)
    pass20plus = models.BigIntegerField(db_column='pass20Plus', blank=True, null=True)
    pass40plus = models.BigIntegerField(db_column='pass40Plus', blank=True, null=True)
    passsacks = models.BigIntegerField(db_column='passSacks', blank=True, null=True)
    passsacky = models.BigIntegerField(db_column='passSackY', blank=True, null=True)
    qbrating = models.FloatField(db_column='qbRating', blank=True, null=True)

    def __str__(self):
        return 'This is only a test.'
    # class Meta:
    #     managed = False
    #     db_table = 'qb_stats'
