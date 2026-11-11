# ORACLES

![Windows](https://img.shields.io/badge/platform-Windows-0078D4)
![Python](https://img.shields.io/badge/Python-3.14-3776AB)
[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue)](LICENSE)

A Windows companion for oracle encounters in Destiny 2's Vault of Glass. Choose your encounter and game-audio input, then follow the detected oracle order on a small overlay.

## What it does

- Supports Templar and Atheon.
- Starts from one executable, with graphical controls and no visible terminals.
- Displays the detected sequence in the app and on an always-on-top overlay.
- Keeps the overlay half-transparent, click-through and fixed in the upper-left corner.
- Shows the encounter map, with numbered sequence markers for Templar.
- Stops the background detector when you select Stop or close the app.

## Getting started

There is no published ORACLES release yet. Build the app using the instructions below, then open `dist/Oracles.exe`. A built copy bundles the detector and assets; the person running it does not need Python.

1. Route the game's audio to a virtual input, such as [VB-CABLE](https://vb-audio.com/Cable/).
2. Open ORACLES and choose **Templar** or **Atheon**.
3. Select the input carrying the game's audio, usually **CABLE Output** with VB-CABLE.
4. Select **Start listening**. Allow the detector time to start before beginning the encounter.
5. Select **Show overlay** to display the map and callouts. Use **Hide overlay** in the main app to hide it.

Keep voices and unrelated audio out of the selected input where possible. ORACLES does not configure Windows audio routing for you.

The overlay is 600 × 330 pixels, positioned 40 pixels from the upper-left corner. It has no border and does not intercept mouse clicks. Borderless or windowed game display may be needed for it to remain visible.

## Build from source

Use Windows with Python 3.14 installed. From the repository root:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
./build.ps1
```

The build produces `dist/Oracles.exe`. Build files and runtime sessions are excluded from Git.

To run the focused tests:

```powershell
.venv/Scripts/python -m unittest discover -s tests -v
```

## Known limitations

ORACLES adds the desktop interface and overlay around an existing audio detector. It does not change that detector's classification logic. Repeated notes and background audio can affect results; a missing or incorrect callout is possible.

Packaged-app checks cover startup, encounter selection, sample audio through VB-CABLE, sequence updates and shutdown. A controlled full-raid accuracy test has not been completed. See [verification notes](VERIFICATION.md) for the exact checks.

## Credits

ORACLES is maintained by [Leah / l3gh](https://github.com/l3gh), with a new graphical launcher, integrated overlay and single-executable packaging.

The audio detector comes from **[Prophet](https://github.com/PyrexPi/prophet), created by [PyrexPi](https://github.com/PyrexPi)**. Thanks also to upstream contributors [dracco1993](https://github.com/dracco1993) and [moverholt5](https://github.com/moverholt5). ORACLES is a separate project and is not presented as their official release.

The supplied Templar map credits **Destiny Raider**. Encounter maps and audio samples were supplied with the upstream tool. Destiny 2 and its game assets belong to **Bungie**. This is an independent community tool.

See [credits and third-party notices](CREDITS.md) for provenance and dependency acknowledgements.

## License

ORACLES code is distributed under [GNU GPLv3](LICENSE), retaining the upstream detector's GPLv3 license. Third-party libraries and game assets retain their respective notices and rights.

The preserved input files are in [`original/`](original/). A pinned copy of the upstream detector source and its license is in [`third_party/detector/`](third_party/detector/); see [source provenance](third_party/detector/PROVENANCE.md) for the distinction between that source snapshot and the supplied binaries.
