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
