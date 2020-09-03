def lowercase_keys(d):
    return dict((k.replace("regularMarket", "").lower(), v) for k, v in d.items())
