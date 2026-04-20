# config/settings/development.py

"""
開発環境専用の設定
本番環境では絶対に使わない
"""

from .base import *  # base.pyの設定を全部引き継ぐ

# 開発中はデバッグモードON（エラー詳細が画面に表示される）
DEBUG = True

# 開発中はローカルホストからのアクセスのみ許可
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 開発用DB（SQLite：ファイル1つで動く軽量DB）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}