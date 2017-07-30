"""utils."""
import os
import shutil
import tempfile
from ngo.conf import settings


class MultiValueDict(dict):
    """key:[value, value, value] な形の辞書を扱う辞書のサブクラス.

    GET、POSTで送信された値は複数の値となっていることもあるため、
    それらを柔軟に扱うためのクラス

    get(key)やitem[key]では、値が複数であっても一つだけ返し
    getlist(key)では、複数の値が詰まったリストを返す
    (値が1つでも、[value]のようなリストで返します)


    <input type="file" name="files" multiple>
    <select name="select" multiple>
    これらのような複数の値を送信するタグには、.getlistでアクセス推奨

    それ以外は、.getやitem[key]で充分です。


    """

    def __init__(self, key_to_list_mapping=()):
        super().__init__(key_to_list_mapping)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, super().__repr__())

    def __getitem__(self, key):
        """item[key]でアクセスした場合に一つだけ値を返す."""
        item = super().__getitem__(key)
        try:
            return item[-1]
        except IndexError:
            return []

    def get(self, key, default=None):
        """item.get(key)でアクセスした場合に一つだけ値を返す."""
        try:
            item = self[key]
        except KeyError:
            return default
        if item == []:
            return default
        return item

    def getlist(self, key, default=None):
        """item.getlist(key)でアクセスした場合にリストとして値を返す."""
        try:
            values = super().__getitem__(key)
        except KeyError:
            if default is None:
                return []
            return default
        return values

    def setlistdefault(self, key, default_list=None):
        """辞書のsetdefaultのリストバージョン."""
        if key not in self:
            if default_list is None:
                default_list = []
            super().__setitem__(key, default_list)
        return self.getlist(key)

    def appendlist(self, key, value):
        """keyに要素をappendする(まだkeyがなければ空リストを作りappend)."""
        self.setlistdefault(key).append(value)


class FileWrapper:
    """アップロードされたファイルをラップするクラス."""

    def __init__(self, file_obj):
        """tempファイルの作成と、ファイル名の保存."""
        self.file_name = file_obj.filename
        self.file = tempfile.NamedTemporaryFile()
        shutil.copyfileobj(file_obj.file, self.file)
        self.file.seek(0)
        file_obj.file.close()

    def save(self, path=None, overwrite=False):
        """pathにファイルを書き込みます."""
        if path is None:
            path = os.path.join(settings.MEDIA_ROOT, self.file_name)
            if not os.path.exists(settings.MEDIA_ROOT):
                os.mkdir(settings.MEDIA_ROOT)
        elif os.path.isdir(path):
            path = os.path.join(path, self.file_name)

        if not overwrite and os.path.exists(path):
            raise IOError('File exists.')
        else:
            with open(path, "wb") as fdst:
                shutil.copyfileobj(self.file, fdst)
            self.file.close()
