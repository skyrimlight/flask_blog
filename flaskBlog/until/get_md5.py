import hashlib


def get_md5(data_str):
    md5 = hashlib.md5(b'xqwp')
    md5.update(data_str.encode('utf-8'))
    return md5.hexdigest()
