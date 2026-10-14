# 版本号统一取自 funlanzou.api（最终来自 pyproject.toml），不在这里留第二份副本：
# funbuild 发版时只会同步 pyproject.toml / script/__version__.md，硬编码的源码
# 副本迟早会和发行元数据对不上。
from funlanzou.api import version

__all__ = ['version']
