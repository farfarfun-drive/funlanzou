import ast
import pickle
import re
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version
from pathlib import Path

import funlanzou.api as api_module
import funlanzou.gui as gui_module
from funlanzou.api import core
from funlanzou.gui import config as config_module

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_credentials_are_written_to_funsecret_not_pickle(monkeypatch):
    secrets = {}

    def write_secret(value, *path):
        secrets[path] = value

    def read_secret(*path):
        return secrets.get(path)

    monkeypatch.setattr(config_module, "write_secret", write_secret)
    monkeypatch.setattr(config_module, "read_secret", read_secret)
    monkeypatch.setattr(config_module, "save_config", lambda config: None)

    config = config_module.Config()
    config.set_infos({
        "name": "audit-user",
        "pwd": "audit-password",
        "cookie": {"session": "audit-cookie"},
    })

    assert config.pwd == "audit-password"
    assert config.cookie == {"session": "audit-cookie"}
    serialized = pickle.dumps(config)
    assert b"audit-password" not in serialized
    assert b"audit-cookie" not in serialized


def test_legacy_credentials_are_removed_after_migration(monkeypatch):
    secrets = {}
    monkeypatch.setattr(
        config_module,
        "write_secret",
        lambda value, *path: secrets.__setitem__(path, value),
    )

    def legacy_encode(value):
        result = bytearray()
        for byte in value.encode("utf-8"):
            encoded = byte ^ config_module.KEY
            result.extend((encoded % 19 + 46, encoded // 19 + 46))
        return result.decode("utf-8")

    config = config_module.Config()
    config._credentials_migrated = False
    config._name = legacy_encode("legacy-user")
    config._pwd = legacy_encode("legacy-password")
    config._cookie = {"session": legacy_encode("legacy-cookie")}
    config._users[config._name] = (
        config._cookie,
        config._name,
        config._pwd,
        -1,
        config.settings,
    )

    assert config.migrate_credentials() is True
    serialized = pickle.dumps(config)
    assert b"legacy-password" not in serialized
    assert b"legacy-cookie" not in serialized
    assert config._pwd == ""
    assert config._cookie == ""


def test_sensitive_response_values_are_not_logged():
    source = open(config_module.__file__.replace("gui/config.py", "api/core.py"), encoding="utf-8").read()
    assert 'logger.debug(f"Set Cookie: acw_sc__v2=' not in source
    assert "filemoreajax.php post.text=" not in source
    assert "filemoreajax.php resp=" not in source


def test_version_manifests_agree():
    """发行元数据与 funbuild 的版本脚本必须一致（SPEC §14.1）。"""
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    declared = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE).group(1)
    assert (REPO_ROOT / "script" / "__version__.md").read_text(encoding="utf-8").strip() == declared


def test_runtime_version_comes_from_distribution_metadata():
    """运行时版本号只能有一个来源，不得在源码里再留硬编码副本。"""
    assert api_module.version is gui_module.version
    try:
        installed = distribution_version("funlanzou")
    except PackageNotFoundError:  # 未安装时只能回退，不应报成真实版本
        assert api_module.version == "0.0.0.dev0"
    else:
        assert api_module.version == installed

    for module in (api_module, gui_module):
        source = Path(module.__file__).read_text(encoding="utf-8")
        assert not re.search(r"^version\s*=\s*['\"]\d", source, re.MULTILINE), (
            f"{module.__name__} 又把版本号写死了，会与 pyproject.toml 漂移"
        )


def test_public_api_has_chinese_docstrings_with_args_and_returns():
    """公开 API 必须有中文 docstring 并说明参数与返回值（SPEC §7）。"""
    tree = ast.parse(Path(core.__file__).read_text(encoding="utf-8"))
    missing = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name.startswith("_"):
            continue
        if not ast.get_docstring(node):
            missing.append(f"class {node.name}")
        for func in node.body:
            if not isinstance(func, ast.FunctionDef) or func.name.startswith("_"):
                continue
            doc = ast.get_docstring(func) or ""
            takes_args = [arg.arg for arg in func.args.args if arg.arg != "self"]
            if not doc:
                missing.append(f"{node.name}.{func.name}: 无 docstring")
                continue
            if takes_args and "Args:" not in doc:
                missing.append(f"{node.name}.{func.name}: 缺 Args")
            if "Returns:" not in doc:
                missing.append(f"{node.name}.{func.name}: 缺 Returns")
    assert not missing, "公开 API 文档缺失: " + "; ".join(missing)
