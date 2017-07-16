"""設定を管理するモジュール."""
import importlib
import os


class Settings:
    """ngoプロジェクトの設定を管理するクラス."""

    def __init__(self):
        """ユーザーの設定をインスタンスの属性へ."""
        # project/settings.pyの設定を格納する
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
