from urllib.parse import urlparse


html = 'https://ru.hexlet.io/projects/51/members/19537?step=3'
res = urlparse(html)
print(res)
print(res.netloc)
print(res.path)