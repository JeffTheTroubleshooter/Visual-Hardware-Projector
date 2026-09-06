# Visual Hardware Projector

Linux program. Drop a JCkernel source zip. Blocks are CPU, MMU, GOP, PIC, NVMe, USB, CSF1. Paste a serial trail like `6kbcdAB2CPqrsD` and the last letter lights the block that died.

This is **not** a live view of the 7290 and **not** CSF1 Viewer.

## Run (Fedora)

```bash
sudo dnf install python3-tkinter
python3 vhp.py
```

Drag `JCkernel-0.0.274-complete.zip` onto the window, paste the QEMU serial line.

`Pqrs` = MMU / CR3 live. Next letter after `D` is IDT then GOP.
