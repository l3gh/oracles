# Verification, 2026-11-11

- Built a Windows GUI-subsystem single-file executable using PyInstaller. The original detector is included as a resource and starts with CREATE_NO_WINDOW, with stdin/stdout/stderr redirected.
- Three unit tests passed: invalid encounter/device rejection, missing detector cleanup/error, and sequence parsing including missing/partial/invalid files.
- Launched the packaged executable and inspected the real desktop window. Encounter and MME input selectors, Start, Stop and Show overlay are graphical controls. VB-CABLE input was enumerated and selected. No terminal window appeared in desktop window inventory.
- Templar packaged-app test: played supplied A, F and D WAV files to the VB-CABLE playback endpoint. The hidden detector wrote 1-2-3 and the real app displayed that sequence.
- Switched to Atheon in the GUI and started a second session. Sequence updates arrived and were displayed. Shared cable audio was not isolated from other applications, so this is not a precise Atheon classification benchmark.
- Stop removed the detector processes. Closing the main window during the second active session also removed the detector processes.
- Original files remain unchanged. No website deployment or public release was performed.
- Final rebuilt executable was launched again. Verified its live sequence display, Templar path markers, and opening/closing the resizable map overlay. The final shared-cable sample run included an earlier background detection followed by 1-2-3; cable input was not exclusively controlled. Main-window Close stopped the detector again.
- PE subsystem is Windows GUI (2), not console. Final local executable is 117,316,149 bytes; SHA-256 `f12cf7f06fc1cc7f5a42e834297f1552be207cdb8d8eb4aff36e5d60042693f0`.

No controlled raid playthrough, clean-PC installation, code-signing or antivirus reputation check is claimed. Existing detector accuracy limitations remain.

## Original overlay restoration

Restored the compact map-left/callouts-right layout and original colors, colored oracle rings and order badges. The overlay is borderless, 50% opaque, fixed at 600×330 at screen +40+40, topmost and click-through. It has no drag/resize controls. Show/Hide overlay in the main app controls visibility.

Native Windows/Tk inspection passed for geometry, opacity, override-redirect and the layered, transparent and no-activate extended styles. Rendered both encounter maps and a Templar 1-2-3 sequence in the native probe. Rebuilt and launched the packaged executable, visually reviewed the restored overlay, and clicked the main app's encounter dropdown through the overlay; the underlying dropdown opened successfully. No detector changes were made. The earlier build fingerprint above is historical and does not identify this rebuilt executable.

Removed the overlay's outer padding, Tk border widths, native frame/edge styles and Windows compositor border. A native probe confirmed no frame/edge flags, zero canvas inset, and retained 50% opacity and click-through. The Windows executable was rebuilt for this change.

Removed the full subtitle beneath the Oracles heading and the old product name from visible error text, current README copy and repository description. Original reference files and the detector's internal filename remain preserved. Rebuilt the windowed executable.

## Detector source comparison, 2026-11-12

Extracted the original executable's embedded `main`, `model` and `resource_path` Python 3.9 code objects. Compiling source files from upstream revision `65f9c587b0f42f7bb292be5cdf8394ba23393710` with CPython 3.9.13 produced matching bytecode, constants, names, variables and flags recursively, excluding file paths and line-number metadata. That revision is preserved in `third_party/detector-matched/`. The previously pinned later revision has a different encounter prompt. Third-party dependency versions and reproducibility of the complete executable remain unverified.
