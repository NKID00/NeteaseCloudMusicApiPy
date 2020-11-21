<h1>
  <p align=center>
    <b>
      NeteaseCloudMusicApiPy
    </b>
  </p>
</h1>

> [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 的 Python 绑定
>
> [API 绑定进度](./TODO.md)（8/208，3.8%）

```python
# 导入 NeteaseCloudMusicApiPy
from ncmapi import ncmapi

# 启动 NeteaseCloudMusicApi 服务进程
# 并创建 NeteaseCloudMusicApi 对象
with ncmapi() as api:
    # 调用手机登录 API
    user_info = api.login_cellphone(13000000000, 'password')
    # 获取当前登录用户的 id
    uid = user_info['account']['id']
    # 调用获取用户歌单 API，获取当前登录用户的歌单并打印
    print(api.user_playlist(uid))
# 退出运行时上下文时自动退出登录并停止服务进程
```

更多代码示例请前往[文档](https://github.com/NKID00/NeteaseCloudMusicApiPy/wiki)

## 特性

- 简单有效地管理服务进程

- Python 风格的使用方式

  - 支持配合运行时上下文（`with` 语句）使用

- 支持使用 Mypy 进行静态类型检查

- 仅支持 Python 3

## 文档

请前往 [Wiki](https://github.com/NKID00/NeteaseCloudMusicApiPy/wiki)

## 版权

NeteaseCloudMusicApiPy 使用 [MIT License](./LICENSE) 进行许可

版权所有 © 2020 NKID00

## 鸣谢

- [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)，MIT License
