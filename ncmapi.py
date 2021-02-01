'''NeteaseCloudMusicApiPy
NeteaseCloudMusicApi 的 Python 绑定
https://github.com/NKID00/NeteaseCloudMusicApiPy

MIT License

Copyright (c) 2020 NKID00

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from typing import Iterable, Dict, Union, Optional
from subprocess import Popen, DEVNULL
from os import environ, kill
from signal import SIGTERM
from contextlib import contextmanager
from time import time
from requests import Session
from hashlib import md5
from base64 import b64decode
from io import BytesIO

__all__ = ['VERSION', 'start_ncmapi_server', 'stop_ncmapi_server',
           'ncmapi', 'NeteaseCloudMusicApi']

VERSION = 'NeteaseCloudMusicApiPy 0.1.0'


def start_ncmapi_server(ncmapi_server_command: Iterable[str],
                        port: int = 3000, host: str = 'localhost') -> int:
    '''启动指定的 NeteaseCloudMusicApi 服务进程并返回进程 pid'''
    env = dict(environ)
    env['HOST'] = str(host)
    env['PORT'] = str(port)
    p = Popen(tuple(ncmapi_server_command), stdin=DEVNULL,
              stdout=DEVNULL, stderr=DEVNULL, env=env)
    return p.pid


def stop_ncmapi_server(ncmapi_server_pid: int) -> None:
    '''停止指定 pid 的 NeteaseCloudMusicApi 服务进程'''
    kill(ncmapi_server_pid, SIGTERM)


@contextmanager
def ncmapi(ncmapi_server_command: Iterable[str],
           port: int = 3000, host: str = 'localhost'):
    '''启动指定的 NeteaseCloudMusicApi 服务进程
    并返回 NeteaseCloudMusicApi 对象
    退出运行时上下文时自动退出登录并停止 NeteaseCloudMusicApi 服务进程'''
    pid = None
    try:
        pid = start_ncmapi_server(ncmapi_server_command, port, host)
        with NeteaseCloudMusicApi(port, host) as api:
            yield api
    finally:
        if pid is not None:
            try:
                stop_ncmapi_server(pid)
            except OSError:
                pass


class NeteaseCloudMusicApi:
    '''保存有 API 地址、相关设置和登录状态的 NeteaseCloudMusicApi 对象
    退出运行时上下文时自动退出登录'''

    def __init__(self, port: int = 3000, host: str = 'localhost',
                 raise_for_status: bool = True, add_timestamp: bool = False):
        self.api_url_base = f'http://{host}:{port}'
        self.api_session = Session()
        self.raise_for_status = raise_for_status
        self.add_timestamp = add_timestamp

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        try:
            self.logout()
        except Exception:
            pass

    def call_api(self, api: str, args: Dict[str, Union[int, bool, str]],
                 add_timestamp: bool = False) -> dict:
        '''调用 API'''
        if self.add_timestamp or add_timestamp:  # 添加时间戳
            args['timestamp'] = int(time() * 1000)
        r = self.api_session.get(self.api_url_base + api, params=args)
        if self.raise_for_status:  # 如果返回错误代码则抛出异常
            r.raise_for_status()
        return r.json()

    def login(self, email: str, password: str = '',
              md5_password: Optional[str] = None,
              **args: Union[int, bool, str]) -> dict:
        '''/login
        邮箱登录
        email: 邮箱
        password: 密码
        md5_password: md5 加密后的密码，传入后 password 将失效'''
        if md5_password is None:
            h = md5()
            h.update(password.encode('utf8'))
            md5_password = h.hexdigest()
        args['email'] = email
        args['md5_password'] = md5_password
        return self.call_api('/login', args, add_timestamp=True)

    def login_cellphone(self, phone: int, password: str = '',
                        countrycode: Optional[int] = None,
                        md5_password: Optional[str] = None,
                        **args: Union[int, bool, str]) -> dict:
        '''/login/cellphone
        手机登录
        phone: 手机号码
        password: 密码
        countrycode: 国家码，用于国外手机号登录，例如美国传入1
        md5_password: md5加密后的密码，传入后 password 将失效'''
        if md5_password is None:
            h = md5()
            h.update(password.encode('utf8'))
            md5_password = h.hexdigest()
        args['phone'] = phone
        if countrycode is not None:
            args['countrycode'] = countrycode
        args['md5_password'] = md5_password
        return self.call_api('/login/cellphone', args, add_timestamp=True)

    def login_qr_check(self, key: str, **args: Union[int, bool, str]) -> dict:
        '''/login/qr/check
        验证二维码登录
        key: 二维码标识符'''
        args['key'] = key
        return self.call_api('/login/qr/check', args, add_timestamp=True)

    def login_qr_create(self, key: str, qrimg: bool = True,
                        qrimg_str: bool = True,
                        **args: Union[int, bool, str]) -> str:
        '''/login/qr/create
        获取二维码链接
        key: 二维码标识符
        qrimg: 获取二维码图片
        qrimg_str: 获取二维码图片字符画'''
        args['key'] = key
        args['qrimg'] = qrimg or qrimg_str
        data = self.call_api('/login/qr/create', args, add_timestamp=True)
        if qrimg_str:
            from PIL import Image
            img_base64 = data['data']['qrimg'].split(',')[1]
            img = Image.open(BytesIO(b64decode(img_base64)))
            img = img.resize((40, 40), Image.NEAREST).crop((1, 1, 39, 39))
            img_str = ''
            for y in range(38):  # 遍历行
                for x in range(38):  # 遍历列
                    black = sum(img.getpixel((x, y))[:3]) < 384
                    img_str += '██' if black else '  '
                img_str += '\n'
            return img_str
        if qrimg:
            return data['data']['qrimg']
        else:
            return data['data']['qrurl']

    def login_qr_key(self, **args: Union[int, bool, str]) -> str:
        '''/login/qr/key
        获取二维码标识符'''
        data = self.call_api('/login/qr/check', args,
                             add_timestamp=True)
        return data['data']['unikey']

    def login_refresh(self, **args: Union[int, bool, str]) -> dict:
        '''/login/refresh
        刷新登录'''
        return self.call_api('/login/refresh', args, add_timestamp=True)

    def login_status(self, **args: Union[int, bool, str]) -> dict:
        '''/login/status
        获取登录状态
        注意: 需要登录'''
        return self.call_api('/login/status', args, add_timestamp=True)

    def logout(self, **args: Union[int, bool, str]) -> dict:
        '''/logout
        退出登录
        注意: 需要登录'''
        return self.call_api('/logout', args, add_timestamp=True)

    def playlist_detail(self, id: int, s: Optional[int] = None,
                        **args: Union[int, bool, str]) -> dict:
        '''/playlist/detail
        获取歌单详情
        id: 歌单 id
        s: 歌单最近的 s 个收藏者[默认8]
        注意: 需要登录'''
        args['id'] = id
        if s:
            args['s'] = s
        return self.call_api('/playlist/detail', args)

    def song_detail(self, ids: Union[int, Iterable[int]],
                    **args: Union[int, bool, str]) -> dict:
        '''/song/detail
        获取歌曲详情
        ids: 音乐 id'''
        if isinstance(ids, int):
            args['ids'] = ids
        else:
            args['ids'] = ','.join(map(str, ids))
        return self.call_api('/song/detail', args)

    def user_playlist(self, uid: int, limit: Optional[int] = None,
                      offset: Optional[int] = None,
                      **args: Union[int, bool, str]) -> dict:
        '''/user/playlist
        获取用户歌单
        uid: 用户 id
        limit: 返回数量
        offset: 偏移数量[默认0]
        注意: 需要登录'''
        args['uid'] = uid
        if limit is not None:
            args['limit'] = limit
        if offset is not None:
            args['offset'] = offset
        return self.call_api('/user/playlist', args)
