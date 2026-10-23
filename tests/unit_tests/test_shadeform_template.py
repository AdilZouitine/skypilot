"""Tests for the Shadeform cluster template."""
import os

import jinja2
import yaml

_TEMPLATE = os.path.join(os.path.dirname(__file__), '..', '..', 'sky',
                         'templates', 'shadeform-ray.yml.j2')


def _render_setup_commands() -> list:
    with open(_TEMPLATE, 'r', encoding='utf-8') as f:
        template = jinja2.Template(f.read())
    content = template.render(num_nodes=1,
                              credentials={},
                              initial_setup_commands=[],
                              ray_skypilot_installation_commands='INSTALL_RAY;')
    return yaml.safe_load(content)['setup_commands']


def test_firewall_is_enabled_before_ray_is_installed():
    setup = _render_setup_commands()[0]

    assert setup.startswith('command -v ufw')
    assert setup.index('sudo ufw default deny incoming') < setup.index(
        'sudo ufw --force enable') < setup.index('INSTALL_RAY;')
    assert 'exit 1' in setup
