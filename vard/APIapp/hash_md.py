import hashlib


def get_hash_md5(filename):
    """
        работает только с файлами,записанными на диске
    """
    try:
        with open(filename, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    except Exception as e:
        pass

