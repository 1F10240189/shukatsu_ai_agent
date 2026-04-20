# apps/companies/models.py

from django.db import models
from apps.accounts.models import User
from apps.offers.models import OfferSiteMaster


class Company(models.Model):
    """
    企業情報
    Gmailから抽出した企業を保存する
    """
    # ユーザーが削除されたとき、紐づく企業も全部削除する
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ユーザー'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='企業名'
    )
    source_site = models.ForeignKey(
        OfferSiteMaster,
        on_delete=models.SET_NULL, # on_delete=models.SET_NULL → 削除されたらNULLにする
        null=True,
        verbose_name='取得元サイト'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='取得日時'
    )

    class Meta:
        db_table = 'companies'
        verbose_name = '企業'
        # 同じユーザーが同じ企業を2重登録できないようにする
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name


class CompanyAnalysis(models.Model):
    """
    AI分析結果
    Gemini APIによる企業分析を保存する
    """
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        verbose_name='企業'
    )
    summary = models.TextField(
        blank=True,
        verbose_name='企業概要'
    )
    salary = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='平均年収（万円）'
    )
    overtime = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='平均残業時間（時間/月）'
    )
    black_score = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='ブラック度（1〜5）'
    )
    raw_response = models.TextField(
        blank=True,
        verbose_name='AIの生レスポンス'
    )
    analyzed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='分析日時'
    )

    class Meta:
        db_table = 'company_analyses'
        verbose_name = '企業分析'

    def __str__(self):
        return f'{self.company.name}の分析'
