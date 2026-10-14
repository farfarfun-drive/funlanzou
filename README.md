# funlanzou

蓝奏云网盘的 API 封装与 PyQt 桌面客户端。

## 安装

作为库使用：

```bash
uv pip install funlanzou
# 或 pip install funlanzou
```

## 使用

```python
from funlanzou.api.core import LanZouCloud

cloud = LanZouCloud()
result = cloud.get_file_info_by_url("https://example.invalid/share", pwd="")
print(result.code)
```

## 弃用迁移

`LanZouCloud.login(username, passwd)` 已弃用。蓝奏云官方登录页改版后，账号密码
登录对多数新账号已失效；请改用 `login_by_cookie()`，并通过
`funlanzou.login_assister` 或浏览器 Cookie 导出获取 Cookie。该方法计划在 `1.0`
（下一次破坏性版本）移除。

包内导入路径 `lanzou` 仍作为兼容层保留，但会发出 `DeprecationWarning`。请将
`import lanzou` 或 `from lanzou...` 迁移为 `import funlanzou` 或
`from funlanzou...`；兼容层计划在 `1.0`（下一次破坏性版本）删除。

## 图形客户端

图形客户端额外依赖 PyQt6 等，需要安装 `gui` extra：

```bash
uv tool install 'funlanzou[gui]'
```

安装完成后运行：

```bash
funlanzou-gui
```

也可以在已安装 `gui` extra 的环境里用模块方式直接启动：

```bash
python -m funlanzou.gui.gui
```

## 致谢

- API 封装基于 [zaxtyson/LanZouCloud-API](https://github.com/zaxtyson/LanZouCloud-API)（MIT 协议）。
- 浏览器 Cookie 读取功能内置了
  [borisbabic/browser_cookie3](https://github.com/borisbabic/browser_cookie3)
  （MIT 协议）。

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
