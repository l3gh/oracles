# Credits

## ORACLES

Leah / [l3gh](https://github.com/l3gh) maintains ORACLES. Changes made in November 2026 include the graphical encounter and input selection, hidden detector lifecycle management, integrated sequence display, compact click-through overlay and Windows executable packaging. The underlying audio classification has not been rewritten.

## Upstream audio detector

The detector is based on [PyrexPi/prophet](https://github.com/PyrexPi/prophet), created by [PyrexPi](https://github.com/PyrexPi) and licensed under GNU GPLv3. Its GitHub contributor list also credits [dracco1993](https://github.com/dracco1993) and [moverholt5](https://github.com/moverholt5), checked on 2026-11-11.

The upstream project's name is retained here for attribution. The name of this application is **ORACLES**.

Upstream source is preserved in [`third_party/detector/`](third_party/detector/) and [`third_party/detector-matched/`](third_party/detector-matched/), including the original license and README. The latter matches the bundled detector's three application modules at Python bytecode level. Its dependency versions and complete build environment remain unverified.

## Maps, samples and game assets

- The Templar map bears the credit **Destiny Raider**. That credit remains intact in the supplied image.
- The Atheon map, note samples and encounter mappings were supplied with the upstream tool. Separate authorship of the Atheon map is not documented in the supplied image or upstream README.
- **Bungie** owns Destiny 2 and its game assets. No endorsement or affiliation is claimed.

## Libraries and tools

ORACLES uses [Python and Tkinter](https://www.python.org/), [Pillow](https://python-pillow.github.io/), [python-sounddevice](https://python-sounddevice.readthedocs.io/) and [PortAudio](https://www.portaudio.com/). Windows packaging uses [PyInstaller](https://pyinstaller.org/). These projects retain their respective licenses.

The legacy detector has its own dependencies, including NumPy, PyAudio and librosa. Its upstream dependency list is retained in [`third_party/detector/requirements.txt`](third_party/detector/requirements.txt).

[VB-CABLE](https://vb-audio.com/Cable/) is an external audio-routing option by VB-Audio Software. It is not included in ORACLES.
