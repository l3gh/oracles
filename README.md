# Oracles

Windows desktop app for Vault of Glass oracle audio detection.

`original/` preserves the complete supplied tool folder, including both executables, audio samples, encounter mappings, maps, readme and the Python map overlay. The original files have not been modified.

## Run

Open `dist/Oracles.exe`. That is the only program you need to launch. It bundles the detector, samples, encounter mappings and map images. Python does not need to be installed on the recipient's PC.

1. Choose Templar or Atheon in the window.
2. Choose the input carrying game audio, usually CABLE Output when using VB-CABLE. Audio routing still needs to be set up separately.
3. Select Start listening. Select Stop to change settings or start another session.

The sequence appears in the app. Show overlay opens the original compact layout: map on the left, encounter and callouts on the right, 50% opacity, borderless, always on top and click-through. It is fixed at 600×330 pixels, 40 pixels from the upper-left corner. Use Hide overlay in the main app to hide it. Closing the main app stops the detector too. The Templar map marks sequence positions and connects them in order using the supplied overlay coordinates. Atheon retains its reference map and numeric sequence.

No terminal is opened and no options need to be typed. The original detector runs as a hidden child process. First startup can take a little while as the bundled Python/audio components load. Stopped sessions retain their last result for reference; starting a new session or changing encounters clears it.

## Build and test

Windows, Python 3.14:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m unittest discover -s tests -v
./build.ps1
```

Source is under `app/`. `build.ps1` produces a single windowed executable in `dist/`. Build output and runtime files stay outside Git. Do not publish the old website ZIP; any future release must use the reviewed new build.

## Limits

This is a new graphical shell around the supplied detector, not a rewrite of its audio classification. It retains the original readme's repeated-note limitation. Samples passed through a virtual cable are a functional check, not proof of accuracy during a raid. No in-game overlay injection is used. The overlay is a normal always-on-top window and may require borderless/windowed game display.

See `VERIFICATION.md` for checks actually performed. Publication remains on hold pending owner review.
