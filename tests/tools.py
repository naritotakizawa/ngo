"""テストのユーティリティー関数群."""
import io
import mimetypes
import os
import uuid


def add_post_environ(environ, data=None, files=None):
    """post用の関数."""
    environ['wsgi.input'] = io.BytesIO()
    boundary = str(uuid.uuid1())
    environ['CONTENT_TYPE'] = 'multipart/form-data; boundary='+boundary
    boundary = '--' + boundary
    body = ''

    # postデータがある場合は書き込む
    if data:
        for tag_name, value in data:
            body += boundary + '\n'
            body += 'Content-Disposition: form-data; name="%s"\n\n' % tag_name
            body += value + '\n'
    # ファイルアップロードがある場合に書き込む
    if files:
        for tag_name, filename, content in files:
            mimetype = str(mimetypes.guess_type(filename)[0]) or 'application/octet-stream'
            body += boundary + '\n'
            body += 'Content-Disposition: file; name="%s"; filename="%s"\n' % \
                 (tag_name, filename)
            body += 'Content-Type: %s\n\n' % mimetype
            body += content + '\n'
    body += boundary + '--\n'
    body = body.encode('utf-8')
    environ['CONTENT_LENGTH'] = str(len(body))
    environ['wsgi.input'].write(body)
    environ['wsgi.input'].seek(0)
    return environ