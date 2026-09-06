# Visual Hardware Projector

One program. Linux app + optional browser page.

Drop a JCkernel source zip. Paste a QEMU serial trail (`6kbcdAB2CPqrsD`). The last letter lights the hardware block that letter belongs to.

Not CSF1 Viewer. Not a live view of the 7290.

## Linux

```bash
sudo dnf install python3-tkinter
python3 vhp.py
# or: python3 vhp.py /path/to/JCkernel-0.0.274-complete.zip
```

## Browser

```bash
python3 -m http.server 8765
# http://127.0.0.1:8765/projector.html
```

## Map

`map.json` — file names and serial letters per block (CPU, MMU, GOP, PIC, NVMe, USB, CSF1).

`Pqrs` = MMU / CR3 live.

The old **JC-Projector** repo is retired. Use this one.
