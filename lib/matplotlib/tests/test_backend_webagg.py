import os
import shutil
import subprocess
import sys
import warnings

import pytest
import matplotlib.backends.backend_webagg_core

import matplotlib.pyplot as plt
from matplotlib.backends.backend_webagg import WebAggApplication
from matplotlib.testing.compare import compare_images, ImageComparisonFailure
from matplotlib.testing.decorators import _image_directories


pytest.importorskip("tornado")


try:
    import pytest_playwright  # noqa
except ImportError:
    @pytest.fixture
    def page():
        pytest.skip(reason='Missing pytest-playwright')


@pytest.mark.parametrize("backend", ["webagg", "nbagg"])
def test_webagg_fallback(backend):
    if backend == "nbagg":
        pytest.importorskip("IPython")
    env = dict(os.environ)
    if os.name != "nt":
        env["DISPLAY"] = ""

    env["MPLBACKEND"] = backend

    test_code = (
        "import os;"
        + f"assert os.environ['MPLBACKEND'] == '{backend}';"
        + "import matplotlib.pyplot as plt; "
        + "print(plt.get_backend());"
        f"assert '{backend}' == plt.get_backend().lower();"
    )
    ret = subprocess.call([sys.executable, "-c", test_code], env=env)

    assert ret == 0


def test_webagg_core_no_toolbar():
    fm = matplotlib.backends.backend_webagg_core.FigureManagerWebAgg
    assert fm._toolbar2_class is None


@pytest.mark.backend('webagg')
def test_webagg_general(random_port, page):
    from playwright.sync_api import expect

    fig, ax = plt.subplots(facecolor='w')

    # Don't start the Tornado event loop, but use the existing event loop
    # started by the `page` fixture.
    WebAggApplication.initialize(port=random_port)
    WebAggApplication.started = True

    page.goto(f'http://{WebAggApplication.address}:{WebAggApplication.port}/')
    expect(page).to_have_title('MPL | WebAgg current figures')

    # Check title.
    expect(page.locator('div.ui-dialog-title')).to_have_text('Figure 1')

    # Check canvas actually contains something.
    baseline_dir, result_dir = _image_directories(test_webagg_general)
    browser = page.context.browser.browser_type.name
    actual = result_dir / f'{browser}.png'
    expected = result_dir / f'{browser}-expected.png'

    canvas = page.locator('canvas.mpl-canvas')
    canvas.screenshot(path=actual)
    shutil.copyfile(baseline_dir / f'{browser}.png', expected)

    err = compare_images(expected, actual, tol=0)
    if err:
        raise ImageComparisonFailure(err)


@pytest.mark.backend('webagg')
@pytest.mark.parametrize('toolbar', ['toolbar2', 'toolmanager'])
def test_webagg_toolbar(random_port, page, toolbar):
    from playwright.sync_api import expect

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='Treat the new Tool classes',
                                category=UserWarning)
        plt.rcParams['toolbar'] = toolbar

    fig, ax = plt.subplots(facecolor='w')

    # Don't start the Tornado event loop, but use the existing event loop
    # started by the `page` fixture.
    WebAggApplication.initialize(port=random_port)
    WebAggApplication.started = True

    page.goto(f'http://{WebAggApplication.address}:{WebAggApplication.port}/')

    expect(page.locator('button.mpl-widget')).to_have_count(
        len([
            name for name, *_ in fig.canvas.manager.ToolbarCls.toolitems
            if name is not None]))

    home = page.locator('button.mpl-widget').nth(0)
    expect(home).to_be_visible()

    back = page.locator('button.mpl-widget').nth(1)
    expect(back).to_be_visible()
    forward = page.locator('button.mpl-widget').nth(2)
    expect(forward).to_be_visible()
    if toolbar == 'toolbar2':
        # ToolManager doesn't implement history button disabling.
        # https://github.com/matplotlib/matplotlib/issues/17979
        expect(back).to_be_disabled()
        expect(forward).to_be_disabled()

    pan = page.locator('button.mpl-widget').nth(3)
    expect(pan).to_be_visible()
    zoom = page.locator('button.mpl-widget').nth(4)
    expect(zoom).to_be_visible()

    save = page.locator('button.mpl-widget').nth(5)
    expect(save).to_be_visible()
    format_dropdown = page.locator('select.mpl-widget')
    expect(format_dropdown).to_be_visible()

    if toolbar == 'toolmanager':
        # Location in status bar is not supported by ToolManager.
        return

    ax.set_position([0, 0, 1, 1])
    bbox = page.locator('canvas.mpl-canvas').bounding_box()
    x, y = bbox['x'] + bbox['width'] / 2, bbox['y'] + bbox['height'] / 2
    page.mouse.move(x, y, steps=2)
    message = page.locator('span.mpl-message')
    expect(message).to_have_text('x=0.500 y=0.500')


@pytest.mark.backend('webagg')
def test_webagg_toolbar_save(random_port, page):
    from playwright.sync_api import expect

    fig, ax = plt.subplots(facecolor='w')

    # Don't start the Tornado event loop, but use the existing event loop
    # started by the `page` fixture.
    WebAggApplication.initialize(port=random_port)
    WebAggApplication.started = True

    page.goto(f'http://{WebAggApplication.address}:{WebAggApplication.port}/')

    save = page.locator('button.mpl-widget').nth(5)
    expect(save).to_be_visible()

    with page.context.expect_page() as new_page_info:
        save.click()
    new_page = new_page_info.value

    new_page.wait_for_load_state()
    assert new_page.url.endswith('download.png')
