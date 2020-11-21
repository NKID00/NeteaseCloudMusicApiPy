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

## 特性

- Python 风格的使用方式

  - 支持配合运行时上下文（`with` 语句）使用

- 支持使用 Mypy 进行静态类型检查

## 使用

```shell
git clone https://github.com/NKID00/NeteaseCloudMusicApiPy.git
```

```python
from ncmapi import ncmapi

# 启动 NeteaseCloudMusicApi 服务进程
with ncmapi() as api:
    user_info: dict = api.login_cellphone(13000000000, 'password')
    uid: int = user_info['account']['id']
    print(api.user_playlist(uid))
# 退出运行时上下文时自动退出登录并停止服务进程
```

更多使用例子请参见文档

## 文档

请前往 [Wiki](https://github.com/NKID00/NeteaseCloudMusicApiPy/wiki)

## 版权

NeteaseCloudMusicApiPy 使用 [MIT License](.\LICENSE) 进行许可

版权所有 © 2020 NKID00

## 鸣谢

- [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)，MIT License
