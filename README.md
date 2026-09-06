# Visual Hardware Projector 0.0.2

One program. Linux app + optional browser page.

This is the first versioned release. It is not CSF1 Viewer. It is not a live camera of the 7290. It is the board that tells you **which real component** a JCkernel source file is talking to, and **where a 64-bit boot trail died**.

## What 0.0.1 does

1. **Probe this computer** — CPU (lm / PAE / hypervisor), RAM, DMI board, UEFI vs BIOS, PCI `vendor:device` + class + Linux driver, block disks, USB ids, DRM connectors. Missing stays N/A.
2. **Import JCkernel source** — zip or folder. Files are matched onto hardware blocks (loader, CPU long mode, MMU, GOP, PIC, PCI CF8/CFC, NVMe, AHCI, USB, CSF1, ACPI, PS/2).
3. **Show machine-code touch lines** — ports (`0xCF8`, `0x3F8`, `0x60`), MMIO (`NVME_MEM_BASE`, GOP FB, LAPIC), CR3 / EFER / ExitBootServices. That is the part only the CPU understands.
4. **Paste a serial trail** (`6kbcdAB2CPqrsD`). Last letter lights the block. Trail letters are decoded.
5. **Paste a physical DIAG dump** from the 7290. PCI ids are pulled out.
6. **Target a known machine** — Latitude 7290 is the default physical target. X1 Carbon Gen 8, T510, A2141, QEMU+OVMF are listed with honest boot status.
7. **Export** `hw_profile.json` + a text report you can keep next to JCkernel as `/Base/Computer/hw_profile.json` (conceptually). The kernel does not read this file yet. The profile is the feed.

## Linux

```bash
sudo dnf install python3-tkinter
python3 vhp.py
python3 vhp.py /path/to/JCkernel-0.0.274-complete.zip
python3 vhp.py --probe --zip JCkernel.zip --trail 6kbcdAB2CPqrsD --export hw_profile.json
```

`--probe` prints the host inventory without a window.

## Update from GitHub

In the app: **Update from GitHub**. That reads

`https://raw.githubusercontent.com/JeffTheTroubleshooter/Visual-Hardware-Projector/main/VERSION`

If GitHub is newer, it downloads `main.zip` and replaces the files listed in `MANIFEST`. No GitHub login. A copy of the old files lands in `.vhp-backup-<oldver>/`. Restart after `vhp.py` itself changes.

```bash
python3 vhp.py --check-update
python3 vhp.py --update
```

## Browser

```bash
python3 -m http.server 8765
# http://127.0.0.1:8765/projector.html
```

The browser cannot read `/sys`. Use it for trail + known-machine + DIAG paste. Host PCI and source-line matching need `vhp.py`.

## Map

`map.json` — one block per component the kernel actually talks to.

`Pqrs` = MMU / CR3 live.  
`t` = GOP mapped after CR3.  
`6` without `k` = jumped at kernel64 and never entered `entry64`.

`known_machines.json` — physical matrix. 7290 NVMe is `8086:F1A8`. iGPU is `8086:5917`. XHCI is `8086:9D2F` driver=none.

## 64-bit use

The projector does not boot the kernel. It tells you which silicon the next edit has to satisfy:

- Host has `lm` + UEFI → long mode is possible on this box.
- Host NVMe class `0108` with a BAR above 4GiB → 32-bit kernel cannot map it. That is why 64-bit is the path.
- Trail last letter names the file to open (`entry64.asm`, `paging.c`, `gop_stamp.c`, `nvme.c`).

Physical proof remains the Dell Latitude 7290 + `USE64` + current `BOOTX64.EFI`. QEMU serial is a crumb trail.

The old **JC-Projector** repo is retired. Use this one.
