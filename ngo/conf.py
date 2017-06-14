"""設定を管理するモジュール."""
import importlib
import os
from ngo import global_settings


class Settings:
    """ngoプロジェクトの設定を管理するクラス."""

    def __init__(self):
        """グローバルな設定と、ユーザーの設定をインスタンスの属性へ."""
        # global_settings.pyの設定を格納する
        # self.DEFAULT_CONTENT_TYPEのようにアクセス可能にする
        for setting in dir(global_settings):
            if setting.isupper():
                setting_value = getattr(global_settings, setting)
                setattr(self, setting, setting_value)

        # project/settings.pyの設定を格納する。被っていた場合は更新
        self.SETTINGS_MODULE = os.environ.get('NGO_SETTINGS_MODULE')
        user_settings = importlib.import_module(self.SETTINGS_MODULE)
        for setting in dir(user_settings):
            if setting.isupper():
                setting_value = getattr(user_settings, setting)
                setattr(self, setting, setting_value)

    def __repr__(self):
        """repr."""
        return '<Settings {}>'.format(self.SETTINGS_MODULE)


settings = Settings()
