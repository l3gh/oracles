# Oracles

Windows desktop work on Prophet, the Vault of Glass oracle audio tool.

`original/` preserves the complete supplied Prophet folder, including both executables, audio samples, encounter mappings, maps, readme and the Python map overlay. The original files have not been modified.

## Current task

Replace terminal-based setup with graphical encounter and audio-device selection. The owner wants one thing to run and no visible terminal windows. Publication and website download packaging are on hold until this desktop work is reviewed.

The audio detector and old interface are supplied as executables; their original source is not present. The map overlay source is available. Investigate the detector's input/output behavior before choosing between a hidden subprocess adapter and a replacement detection component.

## Verification so far

The detector can be started with Windows `CREATE_NO_WINDOW` and captured output. It prints `Choose your encounter file (templar/atheon):`. A short probe that sent `templar` through redirected stdin did not reach a further prompt within 12 seconds. No working graphical launcher or audio detection test is claimed yet.

The original readme requires routed game audio via a virtual microphone and records repeated-note issues in the second oracle wave. Retain those limitations until verified or fixed.
