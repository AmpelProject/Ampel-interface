from pathlib import Path

import pytest

from ampel.cli.AmpelArgumentParser import AmpelArgumentParser


def test_instantiate_with_no_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
):
    env = "AMPEL_CONFIG", "CONDA_PREFIX", "VIRTUAL_ENV"

    with monkeypatch.context() as ctx:
        for var in env:
            ctx.delenv(var, raising=False)
        conf = tmp_path_factory.mktemp("conf") / "conf.yml"
        assert AmpelArgumentParser().has_env_conf is False
        conf.touch()
        assert AmpelArgumentParser().has_env_conf is False
        ctx.setenv("AMPEL_CONFIG", str(conf))
        assert AmpelArgumentParser().has_env_conf is True

    for prefix in env[1:]:
        with monkeypatch.context() as ctx:
            for var in env:
                ctx.delenv(var, raising=False)
            assert AmpelArgumentParser().has_env_conf is False
            tmpdir = tmp_path_factory.mktemp("conf")
            ctx.setenv(prefix, str(tmpdir))
            assert AmpelArgumentParser().has_env_conf is False

            conf = Path(tmpdir) / "share" / "ampel" / "conf.yml"
            assert not conf.exists()
            conf.mkdir(parents=True)
            conf.touch()
            assert conf.exists()

            assert AmpelArgumentParser().has_env_conf is True
