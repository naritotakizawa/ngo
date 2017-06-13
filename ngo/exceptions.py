"""ngoフレームワークの例外を集めたモジュール."""


class NgoException(Exception):
    """ngoフレームワークのルート例外."""
    pass


class Resolver404(NgoException):
    """URLが解決できない場合の例外."""
    pass


class NoReverseMatch(NgoException):
    """reverseができない場合の例外."""
    pass


class TemplateDoesNotExist(NgoException):
    """htmlが見つからない場合の例外."""
    pass
