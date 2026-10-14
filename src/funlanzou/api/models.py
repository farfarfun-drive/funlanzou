"""
容器类，用于储存文件、文件夹，支持 list 的操作，同时支持许多方法方便操作元素
元素类型为 namedtuple，至少拥有 name id 两个属性才能放入容器
"""

from collections.abc import Callable, Iterator
from typing import Any

__all__ = ['FileList', 'FolderList']


class ItemList:
    """具有 name, id 属性对象的列表"""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"<List {', '.join(it.__str__() for it in self)}>"

    def __lt__(self, other: 'ItemList') -> bool:
        """用于路径 List 之间排序"""
        return '/'.join(i.name for i in self) < '/'.join(i.name for i in other)

    @property
    def name_id(self):
        """所有 item 的 name-id 映射，兼容旧版。

        Returns:
            `{名称: id}` 字典；同名元素只保留最后一个。
        """
        return {it.name: it.id for it in self}

    @property
    def all_name(self):
        """所有 item 的 name 列表。

        Returns:
            按容器顺序排列的名称列表。
        """
        return [it.name for it in self]

    def append(self, item: Any) -> None:
        """在末尾插入元素。

        Args:
            item: 至少具有 `name`、`id` 属性的 namedtuple 元素。

        Returns:
            无返回值。
        """
        self._items.append(item)

    def index(self, item: Any) -> int:
        """获取元素在容器中的索引。

        Args:
            item: 容器中的元素。

        Returns:
            元素首次出现的下标；元素不存在时抛 `ValueError`。
        """
        return self._items.index(item)

    def insert(self, pos: int, item: Any) -> None:
        """在指定位置插入元素。

        Args:
            pos: 插入位置，语义与 `list.insert` 相同。
            item: 至少具有 `name`、`id` 属性的 namedtuple 元素。

        Returns:
            无返回值。
        """
        self._items.insert(pos, item)

    def clear(self):
        """清空容器中的所有元素。

        Returns:
            无返回值。
        """
        self._items.clear()

    def filter(self, condition: Callable[[Any], bool]) -> list[Any]:
        """筛选出满足条件的元素。

        Args:
            condition: 判定函数，对元素返回 `True` 表示保留。

        Returns:
            满足条件的元素列表（普通 `list`，不是容器类型）。
        """
        return [it for it in self if condition(it)]

    def find_by_name(self, name: str) -> Any | None:
        """按名称精确搜索元素。

        Args:
            name: 文件或文件夹名称。

        Returns:
            首个名称相同的元素；未找到时返回 `None`。
        """
        for item in self:
            if name == item.name:
                return item
        return None

    def find_by_id(self, fid: int) -> Any | None:
        """按 id 精确搜索元素。

        Args:
            fid: 文件或文件夹 id。

        Returns:
            首个 id 相同的元素；未找到时返回 `None`。
        """
        for item in self:
            if fid == item.id:
                return item
        return None

    def pop_by_id(self, fid: int) -> Any | None:
        """按文件或文件夹 ID 移除并返回首个匹配项。

        Args:
            fid: 要移除的文件或文件夹 ID。

        Returns:
            匹配并移除的元素；未找到时返回 `None`。
        """
        for item in self:
            if item.id == fid:
                self._items.remove(item)
                return item
        return None

    def update_by_id(self, fid: int, **kwargs: Any) -> None:
        """按 id 搜索元素并更新其字段。

        Args:
            fid: 文件或文件夹 id。
            **kwargs: 要覆盖的字段，必须是元素 namedtuple 已有的字段名。

        Returns:
            无返回值。id 不存在时抛 `ValueError`。
        """
        item = self.find_by_id(fid)
        pos = self.index(item)
        data = item._asdict()
        data.update(kwargs)
        self._items[pos] = item.__class__(**data)


class FileList(ItemList):
    """文件列表类"""
    pass


class FolderList(ItemList):
    """文件夹列表类"""
    pass
