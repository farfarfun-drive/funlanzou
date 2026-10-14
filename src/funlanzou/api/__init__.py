from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _distribution_version

from funlanzou.api.core import LanZouCloud

# 版本号的唯一来源是发行元数据（`pyproject.toml`，发版时由 funbuild 递增）。
# 这里不再硬编码：funbuild 只同步 pyproject.toml / script/__version__.md，
# 源码里的副本曾经漂移成 API 报 2.6.8、GUI 报 0.6.8、发行包报 0.2.0。
try:
    version = _distribution_version('funlanzou')
except PackageNotFoundError:  # 未安装、直接从源码树导入时拿不到元数据
    version = '0.0.0.dev0'


def why_error(code: int) -> str:
    """把接口返回的状态码翻译成中文错误原因。

    Args:
        code: `LanZouCloud` 定义的状态码。

    Returns:
        对应的中文错误描述；未收录的状态码返回 `未知错误 {code}`。
    """
    if code == LanZouCloud.URL_INVALID:
        return '分享链接无效'
    elif code == LanZouCloud.LACK_PASSWORD:
        return '缺少提取码'
    elif code == LanZouCloud.PASSWORD_ERROR:
        return '提取码错误'
    elif code == LanZouCloud.FILE_CANCELLED:
        return '分享链接已失效'
    elif code == LanZouCloud.ZIP_ERROR:
        return '解压过程异常'
    elif code == LanZouCloud.NETWORK_ERROR:
        return '网络连接异常'
    elif code == LanZouCloud.CAPTCHA_ERROR:
        return '验证码错误'
    else:
        return f'未知错误 {code}'


__all__ = ['utils', 'types', 'models', 'LanZouCloud', 'version', 'why_error']
