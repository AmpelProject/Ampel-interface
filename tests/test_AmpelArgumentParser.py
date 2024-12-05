from pathlib import Path

import pytest

from ampel.cli.AmpelArgumentParser import AmpelArgumentParser


def test_instantiate_with_no_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
):
    with monkeypatch.context() as ctx:
        conf = tmp_path_factory.mktemp("conf") / "conf.yml"
        conf.touch()
        ctx.setenv("AMPEL_CONFIG", str(conf))
        assert AmpelArgumentParser().has_env_conf is True

    for prefix in "CONDA_PREFIX", "VIRTUAL_ENV":
        with monkeypatch.context() as ctx:
            tmpdir = tmp_path_factory.mktemp("conf")
            ctx.setenv(prefix, str(tmpdir))
            assert AmpelArgumentParser().has_env_conf is False

            conf = Path(tmpdir) / "share" / "ampel" / "conf.yml"
            assert not conf.exists()
            conf.mkdir(parents=True)
            conf.touch()
            assert conf.exists()

            assert AmpelArgumentParser().has_env_conf is True
