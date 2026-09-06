# Changelog

## 0.0.2 — 2026-09-06

- **Update from GitHub** button. Reads public `VERSION` on `JeffTheTroubleshooter/Visual-Hardware-Projector` main, then replaces program files from `main.zip`. No login.
- CLI: `python3 vhp.py --check-update` and `python3 vhp.py --update`.
- Previous copy kept in `.vhp-backup-<oldver>/`. Restart after `vhp.py` changes.

## 0.0.1 — 2026-09-06

First versioned release of Visual Hardware Projector.

- Host probe: CPU flags (lm/PAE/hypervisor), RAM, DMI, UEFI, PCI, storage, USB, DRM.
- Source import: zip or folder. Files matched onto 13 hardware blocks.
- Machine-code touch scan: ports, MMIO bases, CR3/EFER/GOP/NVMe/XHCI symbols.
- Serial trail decode + last-letter projector (kept from the unversioned prototype).
- Known machines: Latitude 7290 (primary), X1 Carbon Gen 8, T510, A2141, QEMU+OVMF.
- DIAG paste PCI-id harvest.
- Export `hw_profile.json` + text report as the feed toward JCkernel compatibility.
- CLI `--probe --zip --trail --export` for headless Fedora.
- Browser page updated to 0.0.1 (trail + target + DIAG; no /sys probe).
