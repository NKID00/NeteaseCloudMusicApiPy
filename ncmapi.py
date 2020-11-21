'''NeteaseCloudMusicApiPy
NeteaseCloudMusicApi 的 Python 绑定
https://github.com/NKID00/NeteaseCloudMusicApiPy
使用 MIT License 进行许可
版权所有 © 2020 NKID00'''

from typing import Iterable, Dict, Union, Optional
from subprocess import Popen, DEVNULL
from os import environ, kill
from signal import SIGTERM
from contextlib import contextmanager
from time import time
from requests import Session
from hashlib import md5

__all__ = ['start_ncmapi_server', 'stop_ncmapi_server',
           'ncmapi', 'NeteaseCloudMusicApi']


def start_ncmapi_server(
        ncmapi_server_command: Iterable[str] = ('node', 'app.js'),
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
def ncmapi(ncmapi_server_command: Iterable[str] = ('node', 'app.js'),
           port: int = 3000, host: str = 'localhost'):
    '''启动指定的 NeteaseCloudMusicApi 服务进程并返回 NeteaseCloudMusicApi 对象
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

    def call_api(self, api: str, args: Dict[str, Union[int, str]]) -> dict:
        '''调用 API'''
        if self.add_timestamp:  # 添加时间戳
            args['timestamp'] = int(time() * 1000)
        r = self.api_session.get(self.api_url_base + api, params=args)
        if self.raise_for_status:  # 如果返回错误代码则抛出异常
            r.raise_for_status()
        return r.json()

    def activate_init_profile(self, **args: Union[int, str]):
        '''/activate/init/profile'''
        return self.call_api('/activate/init/profile', args)

    def album(self, **args: Union[int, str]):
        '''/album'''
        return self.call_api('/album', args)

    def album_detailv(self, **args: Union[int, str]):
        '''/album/detailv'''
        return self.call_api('/album/detailv', args)

    def album_detail_dynamic(self, **args: Union[int, str]):
        '''/album/detail/dynamic'''
        return self.call_api('/album/detail/dynamic', args)

    def album_list(self, **args: Union[int, str]):
        '''/album/list'''
        return self.call_api('/album/list', args)

    def album_list_style(self, **args: Union[int, str]):
        '''/album/list/style'''
        return self.call_api('/album/list/style', args)

    def album_new(self, **args: Union[int, str]):
        '''/album/new'''
        return self.call_api('/album/new', args)

    def album_newest(self, **args: Union[int, str]):
        '''/album/newest'''
        return self.call_api('/album/newest', args)

    def album_sub(self, **args: Union[int, str]):
        '''/album/sub'''
        return self.call_api('/album/sub', args)

    def album_sublist(self, **args: Union[int, str]):
        '''/album/sublist'''
        return self.call_api('/album/sublist', args)

    def album_songsaleboard(self, **args: Union[int, str]):
        '''/album_songsaleboard'''
        return self.call_api('/album_songsaleboard', args)

    def artist_album(self, **args: Union[int, str]):
        '''/artist/album'''
        return self.call_api('/artist/album', args)

    def artist_desc(self, **args: Union[int, str]):
        '''/artist/desc'''
        return self.call_api('/artist/desc', args)

    def artist_list(self, **args: Union[int, str]):
        '''/artist/list'''
        return self.call_api('/artist/list', args)

    def artist_mv(self, **args: Union[int, str]):
        '''/artist/mv'''
        return self.call_api('/artist/mv', args)

    def artist_new_mv(self, **args: Union[int, str]):
        '''/artist/new/mv'''
        return self.call_api('/artist/new/mv', args)

    def artist_new_song(self, **args: Union[int, str]):
        '''/artist/new/song'''
        return self.call_api('/artist/new/song', args)

    def artist_songs(self, **args: Union[int, str]):
        '''/artist/songs'''
        return self.call_api('/artist/songs', args)

    def artist_sub(self, **args: Union[int, str]):
        '''/artist/sub'''
        return self.call_api('/artist/sub', args)

    def artist_sublist(self, **args: Union[int, str]):
        '''/artist/sublist'''
        return self.call_api('/artist/sublist', args)

    def artist_top_song(self, **args: Union[int, str]):
        '''/artist/top/song'''
        return self.call_api('/artist/top/song', args)

    def artists(self, **args: Union[int, str]):
        '''/artists'''
        return self.call_api('/artists', args)

    def avatar_upload(self, **args: Union[int, str]):
        '''/avatar/upload'''
        return self.call_api('/avatar/upload', args)

    def banner(self, **args: Union[int, str]):
        '''/banner'''
        return self.call_api('/banner', args)

    def batch(self, **args: Union[int, str]):
        '''/batch'''
        return self.call_api('/batch', args)

    def calendar(self, **args: Union[int, str]):
        '''/calendar'''
        return self.call_api('/calendar', args)

    def captcha_sent(self, **args: Union[int, str]):
        '''/captcha/sent'''
        return self.call_api('/captcha/sent', args)

    def captcha_verify(self, **args: Union[int, str]):
        '''/captcha/verify'''
        return self.call_api('/captcha/verify', args)

    def cellphone_existence_check(self, **args: Union[int, str]):
        '''/cellphone/existence/check'''
        return self.call_api('/cellphone/existence/check', args)

    def check_music(self, **args: Union[int, str]):
        '''/check/music'''
        return self.call_api('/check/music', args)

    def cloudsearch(self, **args: Union[int, str]):
        '''/cloudsearch'''
        return self.call_api('/cloudsearch', args)

    def comment(self, **args: Union[int, str]):
        '''/comment'''
        return self.call_api('/comment', args)

    def comment_album(self, **args: Union[int, str]):
        '''/comment/album'''
        return self.call_api('/comment/album', args)

    def comment_dj(self, **args: Union[int, str]):
        '''/comment/dj'''
        return self.call_api('/comment/dj', args)

    def comment_event(self, **args: Union[int, str]):
        '''/comment/event'''
        return self.call_api('/comment/event', args)

    def comment_floor(self, **args: Union[int, str]):
        '''/comment/floor'''
        return self.call_api('/comment/floor', args)

    def comment_hot(self, **args: Union[int, str]):
        '''/comment/hot'''
        return self.call_api('/comment/hot', args)

    def comment_hotwall_list(self, **args: Union[int, str]):
        '''/comment/hotwall/list'''
        return self.call_api('/comment/hotwall/list', args)

    def comment_hug_list(self, **args: Union[int, str]):
        '''/comment/hug/list'''
        return self.call_api('/comment/hug/list', args)

    def comment_like(self, **args: Union[int, str]):
        '''/comment/like'''
        return self.call_api('/comment/like', args)

    def comment_music(self, **args: Union[int, str]):
        '''/comment/music'''
        return self.call_api('/comment/music', args)

    def comment_mv(self, **args: Union[int, str]):
        '''/comment/mv'''
        return self.call_api('/comment/mv', args)

    def comment_new(self, **args: Union[int, str]):
        '''/comment/new'''
        return self.call_api('/comment/new', args)

    def comment_playlist(self, **args: Union[int, str]):
        '''/comment/playlist'''
        return self.call_api('/comment/playlist', args)

    def comment_video(self, **args: Union[int, str]):
        '''/comment/video'''
        return self.call_api('/comment/video', args)

    def countries_code_list(self, **args: Union[int, str]):
        '''/countries/code/list'''
        return self.call_api('/countries/code/list', args)

    def daily_signin(self, **args: Union[int, str]):
        '''/daily_signin'''
        return self.call_api('/daily_signin', args)

    def digitalAlbum_ordering(self, **args: Union[int, str]):
        '''/digitalAlbum/ordering'''
        return self.call_api('/digitalAlbum/ordering', args)

    def digitalAlbum_purchased(self, **args: Union[int, str]):
        '''/digitalAlbum/purchased'''
        return self.call_api('/digitalAlbum/purchased', args)

    def dj_banner(self, **args: Union[int, str]):
        '''/dj/banner'''
        return self.call_api('/dj/banner', args)

    def dj_category_excludehot(self, **args: Union[int, str]):
        '''/dj/category/excludehot'''
        return self.call_api('/dj/category/excludehot', args)

    def dj_category_recommend(self, **args: Union[int, str]):
        '''/dj/category/recommend'''
        return self.call_api('/dj/category/recommend', args)

    def dj_catelist(self, **args: Union[int, str]):
        '''/dj/catelist'''
        return self.call_api('/dj/catelist', args)

    def dj_detail(self, **args: Union[int, str]):
        '''/dj/detail'''
        return self.call_api('/dj/detail', args)

    def dj_hot(self, **args: Union[int, str]):
        '''/dj/hot'''
        return self.call_api('/dj/hot', args)

    def dj_paygift(self, **args: Union[int, str]):
        '''/dj/paygift'''
        return self.call_api('/dj/paygift', args)

    def dj_personalize_recommend(self, **args: Union[int, str]):
        '''/dj/personalize/recommend'''
        return self.call_api('/dj/personalize/recommend', args)

    def dj_program(self, **args: Union[int, str]):
        '''/dj/program'''
        return self.call_api('/dj/program', args)

    def dj_program_detail(self, **args: Union[int, str]):
        '''/dj/program/detail'''
        return self.call_api('/dj/program/detail', args)

    def dj_program_toplist(self, **args: Union[int, str]):
        '''/dj/program/toplist'''
        return self.call_api('/dj/program/toplist', args)

    def dj_program_toplist_hours(self, **args: Union[int, str]):
        '''/dj/program/toplist/hours'''
        return self.call_api('/dj/program/toplist/hours', args)

    def dj_radio_hot(self, **args: Union[int, str]):
        '''/dj/radio/hot'''
        return self.call_api('/dj/radio/hot', args)

    def dj_recommend(self, **args: Union[int, str]):
        '''/dj/recommend'''
        return self.call_api('/dj/recommend', args)

    def dj_recommend_type(self, **args: Union[int, str]):
        '''/dj/recommend/type'''
        return self.call_api('/dj/recommend/type', args)

    def dj_sub(self, **args: Union[int, str]):
        '''/dj/sub'''
        return self.call_api('/dj/sub', args)

    def dj_sublist(self, **args: Union[int, str]):
        '''/dj/sublist'''
        return self.call_api('/dj/sublist', args)

    def dj_subscriber(self, **args: Union[int, str]):
        '''/dj/subscriber'''
        return self.call_api('/dj/subscriber', args)

    def dj_today_perfered(self, **args: Union[int, str]):
        '''/dj/today/perfered'''
        return self.call_api('/dj/today/perfered', args)

    def dj_toplist(self, **args: Union[int, str]):
        '''/dj/toplist'''
        return self.call_api('/dj/toplist', args)

    def dj_toplist_hours(self, **args: Union[int, str]):
        '''/dj/toplist/hours'''
        return self.call_api('/dj/toplist/hours', args)

    def dj_toplist_newcomer(self, **args: Union[int, str]):
        '''/dj/toplist/newcomer'''
        return self.call_api('/dj/toplist/newcomer', args)

    def dj_toplist_pay(self, **args: Union[int, str]):
        '''/dj/toplist/pay'''
        return self.call_api('/dj/toplist/pay', args)

    def dj_toplist_popular(self, **args: Union[int, str]):
        '''/dj/toplist/popular'''
        return self.call_api('/dj/toplist/popular', args)

    def event(self, **args: Union[int, str]):
        '''/event'''
        return self.call_api('/event', args)

    def event_del(self, **args: Union[int, str]):
        '''/event/del'''
        return self.call_api('/event/del', args)

    def event_forward(self, **args: Union[int, str]):
        '''/event/forward'''
        return self.call_api('/event/forward', args)

    def fm_trash(self, **args: Union[int, str]):
        '''/fm_trash'''
        return self.call_api('/fm_trash', args)

    def follow(self, **args: Union[int, str]):
        '''/follow'''
        return self.call_api('/follow', args)

    def history_recommend_songs(self, **args: Union[int, str]):
        '''/history/recommend/songs'''
        return self.call_api('/history/recommend/songs', args)

    def history_recommend_songs_detail(
            self, **args: Union[int, str]):
        '''/history/recommend/songs/detail'''
        return self.call_api('/history/recommend/songs/detail', args)

    def homepage_block_page(self, **args: Union[int, str]):
        '''/homepage/block/page'''
        return self.call_api('/homepage/block/page', args)

    def homepage_dragon_ball(self, **args: Union[int, str]):
        '''/homepage/dragon/ball'''
        return self.call_api('/homepage/dragon/ball', args)

    def hot_topic(self, **args: Union[int, str]):
        '''/hot/topic'''
        return self.call_api('/hot/topic', args)

    def hug_comment(self, **args: Union[int, str]):
        '''/hug/comment'''
        return self.call_api('/hug/comment', args)

    def like(self, **args: Union[int, str]):
        '''/like'''
        return self.call_api('/like', args)

    def likelist(self, **args: Union[int, str]):
        '''/likelist'''
        return self.call_api('/likelist', args)

    def login(self, email: str, password: str = '',
              md5_password: Optional[str] = None,
              **args: Union[int, str]):
        '''/login
        邮箱登录
        email: 邮箱
        password: 密码
        md5_password: md5 加密后的密码，传入后 password 将失效
        '''
        if md5_password is None:
            h = md5()
            h.update(password.encode('utf8'))
            md5_password = h.hexdigest()
        args['email'] = email
        args['md5_password'] = md5_password
        return self.call_api('/login', args)

    def login_cellphone(self, phone: int, password: str = '',
                        countrycode: Optional[int] = None,
                        md5_password: Optional[str] = None,
                        **args: Union[int, str]):
        '''/login/cellphone
        手机登录
        phone: 手机号码
        password: 密码
        countrycode: 国家码，用于国外手机号登录，例如美国传入：1
        md5_password: md5加密后的密码,传入后 password 将失效 '''
        if md5_password is None:
            h = md5()
            h.update(password.encode('utf8'))
            md5_password = h.hexdigest()
        args['phone'] = phone
        if countrycode is not None:
            args['countrycode'] = countrycode
        args['md5_password'] = md5_password
        return self.call_api('/login/cellphone', args)

    def login_refresh(self, **args: Union[int, str]):
        '''/login/refresh
        刷新登录'''
        return self.call_api('/login/refresh', args)

    def login_status(self, **args: Union[int, str]):
        '''/login/status
        登录状态
        注意: 需要登录'''
        return self.call_api('/login/status', args)

    def logout(self, **args: Union[int, str]):
        '''/logout
        退出登录
        注意: 需要登录'''
        return self.call_api('/logout', args)

    def lyric(self, **args: Union[int, str]):
        '''/lyric'''
        return self.call_api('/lyric', args)

    def msg_comments(self, **args: Union[int, str]):
        '''/msg/comments'''
        return self.call_api('/msg/comments', args)

    def msg_forwards(self, **args: Union[int, str]):
        '''/msg/forwards'''
        return self.call_api('/msg/forwards', args)

    def msg_notices(self, **args: Union[int, str]):
        '''/msg/notices'''
        return self.call_api('/msg/notices', args)

    def msg_private(self, **args: Union[int, str]):
        '''/msg/private'''
        return self.call_api('/msg/private', args)

    def msg_private_history(self, **args: Union[int, str]):
        '''/msg/private/history'''
        return self.call_api('/msg/private/history', args)

    def msg_recentcontact(self, **args: Union[int, str]):
        '''/msg/recentcontact'''
        return self.call_api('/msg/recentcontact', args)

    def mv(self, **args: Union[int, str]):
        '''/mv'''
        return self.call_api('/mv', args)

    def mv_all(self, **args: Union[int, str]):
        '''/mv/all'''
        return self.call_api('/mv/all', args)

    def mv_detail(self, **args: Union[int, str]):
        '''/mv/detail'''
        return self.call_api('/mv/detail', args)

    def mv_detail_info(self, **args: Union[int, str]):
        '''/mv/detail/info'''
        return self.call_api('/mv/detail/info', args)

    def mv_exclusive_rcmd(self, **args: Union[int, str]):
        '''/mv/exclusive/rcmd'''
        return self.call_api('/mv/exclusive/rcmd', args)

    def mv_first(self, **args: Union[int, str]):
        '''/mv/first'''
        return self.call_api('/mv/first', args)

    def mv_sub(self, **args: Union[int, str]):
        '''/mv/sub'''
        return self.call_api('/mv/sub', args)

    def mv_sublist(self, **args: Union[int, str]):
        '''/mv/sublist'''
        return self.call_api('/mv/sublist', args)

    def mv_url(self, **args: Union[int, str]):
        '''/mv/url'''
        return self.call_api('/mv/url', args)

    def personal_fm(self, **args: Union[int, str]):
        '''/personal_fm'''
        return self.call_api('/personal_fm', args)

    def personalized(self, **args: Union[int, str]):
        '''/personalized'''
        return self.call_api('/personalized', args)

    def personalized_djprogram(self, **args: Union[int, str]):
        '''/personalized/djprogram'''
        return self.call_api('/personalized/djprogram', args)

    def personalized_mv(self, **args: Union[int, str]):
        '''/personalized/mv'''
        return self.call_api('/personalized/mv', args)

    def personalized_newsong(self, **args: Union[int, str]):
        '''/personalized/newsong'''
        return self.call_api('/personalized/newsong', args)

    def personalized_privatecontent(
            self, **args: Union[int, str]):
        '''/personalized/privatecontent'''
        return self.call_api('/personalized/privatecontent', args)

    def personalized_privatecontent_list(
            self, **args: Union[int, str]):
        '''/personalized/privatecontent/list'''
        return self.call_api('/personalized/privatecontent/list', args)

    def playlist_catlist(self, **args: Union[int, str]):
        '''/playlist/catlist'''
        return self.call_api('/playlist/catlist', args)

    def playlist_cover_update(self, **args: Union[int, str]):
        '''/playlist/cover/update'''
        return self.call_api('/playlist/cover/update', args)

    def playlist_create(self, **args: Union[int, str]):
        '''/playlist/create'''
        return self.call_api('/playlist/create', args)

    def playlist_delete(self, **args: Union[int, str]):
        '''/playlist/delete'''
        return self.call_api('/playlist/delete', args)

    def playlist_desc_update(self, **args: Union[int, str]):
        '''/playlist/desc/update'''
        return self.call_api('/playlist/desc/update', args)

    def playlist_detail(self, id: int, s: Optional[int] = None,
                        **args: Union[int, str]):
        '''/playlist/detail
        获取歌单详情
        id: 歌单 id
        s: 歌单最近的 s 个收藏者[默认8]
        注意: 需要登录'''
        args['id'] = id
        if s:
            args['s'] = s
        return self.call_api('/playlist/detail', args)

    def playlist_highquality_tags(self, **args: Union[int, str]):
        '''/playlist/highquality/tags'''
        return self.call_api('/playlist/highquality/tags', args)

    def playlist_hot(self, **args: Union[int, str]):
        '''/playlist/hot'''
        return self.call_api('/playlist/hot', args)

    def playlist_mylike(self, **args: Union[int, str]):
        '''/playlist/mylike'''
        return self.call_api('/playlist/mylike', args)

    def playlist_name_update(self, **args: Union[int, str]):
        '''/playlist/name/update'''
        return self.call_api('/playlist/name/update', args)

    def playlist_order_update(self, **args: Union[int, str]):
        '''/playlist/order/update'''
        return self.call_api('/playlist/order/update', args)

    def playlist_subscribe(self, **args: Union[int, str]):
        '''/playlist/subscribe'''
        return self.call_api('/playlist/subscribe', args)

    def playlist_subscribers(self, **args: Union[int, str]):
        '''/playlist/subscribers'''
        return self.call_api('/playlist/subscribers', args)

    def playlist_tags_update(self, **args: Union[int, str]):
        '''/playlist/tags/update'''
        return self.call_api('/playlist/tags/update', args)

    def playlist_track_add(self, **args: Union[int, str]):
        '''/playlist/track/add'''
        return self.call_api('/playlist/track/add', args)

    def playlist_track_delete(self, **args: Union[int, str]):
        '''/playlist/track/delete'''
        return self.call_api('/playlist/track/delete', args)

    def playlist_tracks(self, **args: Union[int, str]):
        '''/playlist/tracks'''
        return self.call_api('/playlist/tracks', args)

    def playlist_update(self, **args: Union[int, str]):
        '''/playlist/update'''
        return self.call_api('/playlist/update', args)

    def playlist_video_recent(self, **args: Union[int, str]):
        '''/playlist/video/recent'''
        return self.call_api('/playlist/video/recent', args)

    def playmode_intelligence_list(
            self, **args: Union[int, str]):
        '''/playmode/intelligence/list'''
        return self.call_api('/playmode/intelligence/list', args)

    def program_recommend(self, **args: Union[int, str]):
        '''/program/recommend'''
        return self.call_api('/program/recommend', args)

    def rebind(self, **args: Union[int, str]):
        '''/rebind'''
        return self.call_api('/rebind', args)

    def recommend_resource(self, **args: Union[int, str]):
        '''/recommend/resource'''
        return self.call_api('/recommend/resource', args)

    def recommend_songs(self, **args: Union[int, str]):
        '''/recommend/songs'''
        return self.call_api('/recommend/songs', args)

    def register_cellphone(self, **args: Union[int, str]):
        '''/register/cellphone'''
        return self.call_api('/register/cellphone', args)

    def related_allvideo(self, **args: Union[int, str]):
        '''/related/allvideo'''
        return self.call_api('/related/allvideo', args)

    def related_playlist(self, **args: Union[int, str]):
        '''/related/playlist'''
        return self.call_api('/related/playlist', args)

    def resource_like(self, **args: Union[int, str]):
        '''/resource/like'''
        return self.call_api('/resource/like', args)

    def scrobble(self, **args: Union[int, str]):
        '''/scrobble'''
        return self.call_api('/scrobble', args)

    def search(self, **args: Union[int, str]):
        '''/search'''
        return self.call_api('/search', args)

    def search_default(self, **args: Union[int, str]):
        '''/search/default'''
        return self.call_api('/search/default', args)

    def search_hot(self, **args: Union[int, str]):
        '''/search/hot'''
        return self.call_api('/search/hot', args)

    def search_hot_detail(self, **args: Union[int, str]):
        '''/search/hot/detail'''
        return self.call_api('/search/hot/detail', args)

    def search_multimatch(self, **args: Union[int, str]):
        '''/search/multimatch'''
        return self.call_api('/search/multimatch', args)

    def search_suggest(self, **args: Union[int, str]):
        '''/search/suggest'''
        return self.call_api('/search/suggest', args)

    def send_playlist(self, **args: Union[int, str]):
        '''/send/playlist'''
        return self.call_api('/send/playlist', args)

    def send_song(self, **args: Union[int, str]):
        '''/send/song'''
        return self.call_api('/send/song', args)

    def send_text(self, **args: Union[int, str]):
        '''/send/text'''
        return self.call_api('/send/text', args)

    def setting(self, **args: Union[int, str]):
        '''/setting'''
        return self.call_api('/setting', args)

    def share_resource(self, **args: Union[int, str]):
        '''/share/resource'''
        return self.call_api('/share/resource', args)

    def simi_artist(self, **args: Union[int, str]):
        '''/simi/artist'''
        return self.call_api('/simi/artist', args)

    def simi_mv(self, **args: Union[int, str]):
        '''/simi/mv'''
        return self.call_api('/simi/mv', args)

    def simi_playlist(self, **args: Union[int, str]):
        '''/simi/playlist'''
        return self.call_api('/simi/playlist', args)

    def simi_song(self, **args: Union[int, str]):
        '''/simi/song'''
        return self.call_api('/simi/song', args)

    def simi_user(self, **args: Union[int, str]):
        '''/simi/user'''
        return self.call_api('/simi/user', args)

    def song_detail(self, ids: Union[int, Iterable[int]],
                    **args: Union[int, str]):
        '''/song/detail
        获取歌曲详情
        ids: 音乐 id'''
        if isinstance(ids, int):
            args['ids'] = ids
        else:
            args['ids'] = ','.join(map(str, ids))
        return self.call_api('/song/detail', args)

    def song_order_update(self, **args: Union[int, str]):
        '''/song/order/update'''
        return self.call_api('/song/order/update', args)

    def song_url(self, **args: Union[int, str]):
        '''/song/url'''
        return self.call_api('/song/url', args)

    def top_album(self, **args: Union[int, str]):
        '''/top/album'''
        return self.call_api('/top/album', args)

    def top_artists(self, **args: Union[int, str]):
        '''/top/artists'''
        return self.call_api('/top/artists', args)

    def top_list(self, **args: Union[int, str]):
        '''/top/list'''
        return self.call_api('/top/list', args)

    def top_mv(self, **args: Union[int, str]):
        '''/top/mv'''
        return self.call_api('/top/mv', args)

    def top_playlist(self, **args: Union[int, str]):
        '''/top/playlist'''
        return self.call_api('/top/playlist', args)

    def top_playlist_highquality(self, **args: Union[int, str]):
        '''/top/playlist/highquality'''
        return self.call_api('/top/playlist/highquality', args)

    def top_song(self, **args: Union[int, str]):
        '''/top/song'''
        return self.call_api('/top/song', args)

    def topic_sublist(self, **args: Union[int, str]):
        '''/topic/sublist'''
        return self.call_api('/topic/sublist', args)

    def toplist(self, **args: Union[int, str]):
        '''/toplist'''
        return self.call_api('/toplist', args)

    def toplist_artist(self, **args: Union[int, str]):
        '''/toplist/artist'''
        return self.call_api('/toplist/artist', args)

    def toplist_detail(self, **args: Union[int, str]):
        '''/toplist/detail'''
        return self.call_api('/toplist/detail', args)

    def user_account(self, **args: Union[int, str]):
        '''/user/account'''
        return self.call_api('/user/account', args)

    def user_audio(self, **args: Union[int, str]):
        '''/user/audio'''
        return self.call_api('/user/audio', args)

    def user_binding(self, **args: Union[int, str]):
        '''/user/binding'''
        return self.call_api('/user/binding', args)

    def user_cloud(self, **args: Union[int, str]):
        '''/user/cloud'''
        return self.call_api('/user/cloud', args)

    def user_cloud_del(self, **args: Union[int, str]):
        '''/user/cloud/del'''
        return self.call_api('/user/cloud/del', args)

    def user_cloud_detail(self, **args: Union[int, str]):
        '''/user/cloud/detail'''
        return self.call_api('/user/cloud/detail', args)

    def user_detail(self, **args: Union[int, str]):
        '''/user/detail'''
        return self.call_api('/user/detail', args)

    def user_dj(self, **args: Union[int, str]):
        '''/user/dj'''
        return self.call_api('/user/dj', args)

    def user_event(self, **args: Union[int, str]):
        '''/user/event'''
        return self.call_api('/user/event', args)

    def user_followeds(self, **args: Union[int, str]):
        '''/user/followeds'''
        return self.call_api('/user/followeds', args)

    def user_follows(self, **args: Union[int, str]):
        '''/user/follows'''
        return self.call_api('/user/follows', args)

    def user_level(self, **args: Union[int, str]):
        '''/user/level'''
        return self.call_api('/user/level', args)

    def user_playlist(self, uid: int, limit: Optional[int] = None,
                      offset: Optional[int] = None,
                      **args: Union[int, str]):
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

    def user_record(self, **args: Union[int, str]):
        '''/user/record'''
        return self.call_api('/user/record', args)

    def user_replacephone(self, **args: Union[int, str]):
        '''/user/replacephone'''
        return self.call_api('/user/replacephone', args)

    def user_subcount(self, **args: Union[int, str]):
        '''/user/subcount'''
        return self.call_api('/user/subcount', args)

    def user_update(self, **args: Union[int, str]):
        '''/user/update'''
        return self.call_api('/user/update', args)

    def video_category_list(self, **args: Union[int, str]):
        '''/video/category/list'''
        return self.call_api('/video/category/list', args)

    def video_detail(self, **args: Union[int, str]):
        '''/video/detail'''
        return self.call_api('/video/detail', args)

    def video_detail_info(self, **args: Union[int, str]):
        '''/video/detail/info'''
        return self.call_api('/video/detail/info', args)

    def video_group(self, **args: Union[int, str]):
        '''/video/group'''
        return self.call_api('/video/group', args)

    def video_group_list(self, **args: Union[int, str]):
        '''/video/group/list'''
        return self.call_api('/video/group/list', args)

    def video_sub(self, **args: Union[int, str]):
        '''/video/sub'''
        return self.call_api('/video/sub', args)

    def video_timeline_all(self, **args: Union[int, str]):
        '''/video/timeline/all'''
        return self.call_api('/video/timeline/all', args)

    def video_timeline_recommend(self, **args: Union[int, str]):
        '''/video/timeline/recommend'''
        return self.call_api('/video/timeline/recommend', args)

    def video_url(self, **args: Union[int, str]):
        '''/video/url'''
        return self.call_api('/video/url', args)

    def yunbei(self, **args: Union[int, str]):
        '''/yunbei'''
        return self.call_api('/yunbei', args)

    def yunbei_info(self, **args: Union[int, str]):
        '''/yunbei/info'''
        return self.call_api('/yunbei/info', args)

    def yunbei_sign(self, **args: Union[int, str]):
        '''/yunbei/sign'''
        return self.call_api('/yunbei/sign', args)

    def yunbei_task_finish(self, **args: Union[int, str]):
        '''/yunbei/task/finish'''
        return self.call_api('/yunbei/task/finish', args)

    def yunbei_tasks(self, **args: Union[int, str]):
        '''/yunbei/tasks'''
        return self.call_api('/yunbei/tasks', args)

    def yunbei_tasks_expense(self, **args: Union[int, str]):
        '''/yunbei/tasks/expense'''
        return self.call_api('/yunbei/tasks/expense', args)

    def yunbei_tasks_receipt(self, **args: Union[int, str]):
        '''/yunbei/tasks/receipt'''
        return self.call_api('/yunbei/tasks/receipt', args)

    def yunbei_tasks_todo(self, **args: Union[int, str]):
        '''/yunbei/tasks/todo'''
        return self.call_api('/yunbei/tasks/todo', args)

    def yunbei_today(self, **args: Union[int, str]):
        '''/yunbei/today'''
        return self.call_api('/yunbei/today', args)
