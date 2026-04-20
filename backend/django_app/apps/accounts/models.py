from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    カスタムユーザーモデル
    Djangoの標準Userを継承して拡張する
    """
    # AbstractUserが持っている標準フィールド
    # username, email, password, created_at など

    # 将来的に追加できるように空で作っておく
    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'

    def __str__(self):
        return self.email