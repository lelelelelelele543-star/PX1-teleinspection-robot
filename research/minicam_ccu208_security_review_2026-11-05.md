# Mini-Cam Proteus / CCU208 — preliminary security review (2026-11-05)

**Status: passive review only; no confirmed vulnerability.**
**Purpose:** understand the reference system for PX1 and assess the security of an owner's CCU, without touching any vendor infrastructure.

## Evidence inventory and limitations

| Item | Verified | Not verified |
|---|---|---|
| Owner's SD-image backup | A file named `ЛП.imgc` exists in the owner's private Drive, 2,933,868,241 bytes. The owner confirms it is a backup made from a Mini-Cam control unit SD card. | The raw contents, image magic, partitions, boot files and firmware have **not** been inspected. |
| Offline retrieval | The connected Drive tool refused to transfer the 2.93 GB file due to a 268,435,456-byte limit. | No partial/random-access binary reads are available through the current connector. |
| Public manufacturer documentation | CCU208 functionality and relevant interfaces are documented below. | No OS, package version, or security weakness can be attributed to this specific unit from public docs alone. |

**Important distinction:** CCU208 manuals distinguish internal solid-state storage (at least 32 GB) from removable SD/USB used to copy survey records. A copy from an SD card may contain *only* exported surveys rather than the bootable OS, unless the exact card origin/partitions are proven by examination.

## Documented interfaces — *review targets, not vulnerabilities*

1. **Removable USB/SD media:** CCU208 exports and imports recorded videos, photographs, project data. Investigate file parsing and update validation only on an isolated owner-controlled test image.
2. **Wi-Fi and Windows file sharing:** manual describes joining a local Wi-Fi network and browsing a network share called `CCU Memory` via Windows Explorer and a UNC path. This establishes a network file-sharing surface; it does **not** establish anonymous access, a specific SMB version, or a flaw.
3. **Network/cloud/reporting workflow:** manual documents uploading WinCan projects, sending reports by email, and that the WinCanWeb login/password are retained after power-down. Determine protection of saved credentials *offline* when data is obtainable; do not publish extracted values.
4. **Software update workflow:** a software-update function is offered in the CCU setup UI. Any update-file security evaluation requires the actual update package or firmware image.
5. **Controls and physical safety:** joystick/crawler actions and emergency stop are documented. Avoid live fuzzing or command injection against powered machinery.

## Versions and CVEs

- Minicam Proteus manual states software revision **3.3.6 (2017-09-06)** or newer is needed for the RCP4 pairing feature. That is a historical *minimum feature requirement*, **not** a verified installed version.
- **CVE-2026-5495** concerns **Labcenter Electronics Proteus 8.17 SP5** (PDSPRJ parsing / out-of-bounds write) and is **not** evidence of a vulnerability in Mini-Cam Proteus.
- No specific CVE for the owner's Mini-Cam device is verified in this review. A clean public-CVE search is not a guarantee of product security.

## Offline examination plan (blocked on safely accessing bytes)

1. Confirm `.imgc` container header and decompression method from the actual file bytes.
2. Decompress a *read-only copy*; inventory disk partition table, filesystems, timestamps and executables, and record cryptographic hashes.
3. Determine whether it is survey-only media or boot/storage media.
4. If there is firmware: identify operating system, package versions, services, WinCan/ProPIPE components, Wi-Fi and network-share configuration, and updater signatures.
5. Check verified component versions against authoritative vendor advisories / CVE entries; distinguish confirmed exposure from speculation.
6. Produce a redacted report that does **not** include credentials, tokens, customer data or proprietary raw files. Test suspected issues only on an isolated system owned/authorized by the operator.

## Evidence links

- Mini-Cam Proteus Instruction Manual, Version L: https://www.minicam.co.uk/wp-content/uploads/2022/04/Proteus_Version-L_EN-2022-RL.pdf (CCU208 p.44–67; Wi-Fi p.60–65)
- Mini-Cam CCU208 brochure: https://www.minicam.co.uk/wp-content/uploads/2022/04/CCU208-1.pdf
- Product page: https://www.minicam.co.uk/products/control-units/proteus-control-unit/
- ZDI-26-257 (unrelated Labcenter CVE): https://www.zerodayinitiative.com/advisories/ZDI-26-257/

**Scope safety:** no active scans, login attempts, exploitation, or access to Mini-Cam Ltd's servers were undertaken. The SD image remains private and unchanged.

## Update: owner-operated Colab triage completed (2026-11-05)

The owner executed the offline triage in Google Colab and saved `PX1_SD_REPORT.txt` to private Google Drive. The report confirms:

- Source file: `ЛП.imgc` (compressed file 2,933,868,241 bytes).
- IMGC format/header recognized by `unimgc`.
- 16,777,216 decoded bytes examined.
- MBR boot signature `55 AA` detected.
- MBR partition 1: type `0x83` (conventionally Linux), start LBA 64260, length 15,454,530 sectors. With 512-byte sectors this begins 32,901,120 bytes (~31.4 MiB) into the decoded disk and describes ~7.91 GB of partition data.
- The partition begins **after** the first 16 MiB examined, so filesystem type and OS version remain unknown. This is **not** a verified Linux installation and not a verified vulnerability.

Next authorized offline step is to inspect the filesystem signature at the partition offset and, if possible, examine the root filesystem on a read-only copy in the owner's private environment. Do not upload original data, credential material, customer inspections, or proprietary firmware to this public repository.

## Additional forensic observation (derived from first 16 bytes)

The owner's initial report lists the raw disk image prefix as `0e 02 00 ea ...`. Interpreted as a **little-endian ARM32 instruction**, the initial four bytes form `0xEA00020E`, which decodes as an unconditional ARM `B` with a branch destination at offset `0x840` (assuming code starts at address 0). This is **consistent with a bootloader or executable boot sector**, which strengthens but does not prove the hypothesis that the SD card is boot-related rather than survey-only media. The same bytes alone cannot reliably identify the actual processor, OS, or vulnerability. Do **not** conflate this hypothesis with a verified installed Linux/ARM version.

A second, **read-only**, phone-triggerable Colab probe has been added: [PX1_SD_FS_Colab.ipynb](PX1_SD_FS_Colab.ipynb). It reads only 34 MiB of decompressed stream to check the filesystem superblock at sector 64260 and writes `PX1_SD_FS_REPORT.txt` privately on Drive; it neither extracts customer material nor uploads raw firmware to GitHub. The resulting report has **not yet** been received or inspected.

## Filesystem verification from owner's second Colab run

The private `PX1_SD_FS_REPORT.txt` confirms that partition 1 has an ext-family filesystem. Start offset: 32901120 bytes; size: 7912719360 bytes; block size: 4096 bytes; inode count: 483328; volume label: `linux_ltib`. LTIB is a Linux image build framework associated with Freescale/NXP. The label is suggestive only; the system and chipset have not been identified. No vulnerabilities have been confirmed. Source: https://www.nxp.com/docs/en/application-note/AN4426.pdf

## Third owner-operated offline analysis (2026-11-05)

The user ran the read-only Google Colab extractor and provided private `PX1_SD_OS_REPORT.txt` via connected Drive. Verified metadata (no customer data or credentials published):

- Linux filesystem root includes `/bin`, `/boot`, `/etc`, `/lib`, `/sbin`, `/usr`.
- `/boot`: `u-boot.bin`, `zImage`, `vmlinux`, `uImage`, `System.map`, `linux.config`. A separate `u-boot-mx53-loco.bin` also exists at the filesystem root.
- `/lib/modules/2.6.35.3-1129-g691c08a` names a **Linux kernel 2.6.35.3-based module ABI**; installation/running-kernel status cannot be verified from disk contents alone.
- `/etc/issue` identifies Freescale Semiconductor, an ARM GNU EABI toolchain GCC 4.4.4, and a root-filesystem build timestamp in February 2012.
- `/etc/ltib-release` identifies LTIB release date May 2015 and application version `9.1.1`.
- `/bin/busybox` has an **ARM ELF** header.
- `u-boot-mx53-loco.bin` is the filename Freescale uses for the **i.MX53 START/LOCO reference board**. This is strong evidence of an i.MX53 software lineage but is **not proof of the physical SoC** in this exact CCU.

Security triage: **CVE-2016-5195 (Dirty COW)** is a *version-range candidate* for the legacy 2.6.35 kernel family, based on the upstream affected range and the local privilege-escalation nature of the flaw. Its presence in the owner image is **not confirmed** because vendor backports, actual running kernel, reachability and any mitigations remain unknown. There has been no exploit execution or testing against vendor infrastructure.

Authoritative references:
- i.MX53 START Linux Demo Image Readme: https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/10054/2/478-i.MX53_START_Linux_DemoImage_Readme.pdf
- Dirty COW: https://nvd.nist.gov/vuln/detail/CVE-2016-5195
- US-CERT: https://www.kb.cert.org/vuls/id/243144

## i.MX53 BSP comparison / passive fourth step (2026-11-05)

Comparison of the private SD report with Freescale's official *i.MX53 START Linux Release Notes Rev 11.09.02* gives three matching traits:

- Both the private image and Freescale's reference package include a file called `u-boot-mx53-loco.bin`.
- Both include Linux **2.6.35.3**-family software and ARM.
- The Freescale BSP release includes **GCC 4.4.4**, LTIB, a U-Boot bootloader and an SD/MMC boot workflow, consistent with the image's `/etc/issue` and `/etc/ltib-release` evidence.

Official reference: https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/80907/1/i.MX53_START_Linux_BSP_Release_Note.pdf .

This is good evidence of **Freescale i.MX53 BSP lineage**, but does **not prove** the actual device SoC, loaded bootloader, or any manufacturer's firmware vulnerability. The file label `linux_ltib` and application version `9.1.1` refer to the firmware image's build metadata; they must not be confused with a Mini-Cam CCU application version.

For CVE-2016-5195 (Dirty COW), the **upstream** kernel family is in the affected version range. Local privilege escalation is possible in **unpatched, running** affected kernels. It cannot be asserted for Mini-Cam without checking vendor patches and the booted kernel; no exploit or active attack is part of this analysis. Upstream advisory: https://nvd.nist.gov/vuln/detail/CVE-2016-5195 .

A fourth read-only Colab inventory notebook was created: [PX1_SD_Inventory_Colab.ipynb](PX1_SD_Inventory_Colab.ipynb). This notebook reports selected directory names and kernel configuration flags from an owner-controlled offline copy. The owner must initiate execution in their own Colab session. Its resulting report is not yet available.

## Additional upstream CVE version-screening (not device findings)

The Linux module directory in the offline image refers to a 2.6.35.3-derived kernel. Two upstream issues overlap this old kernel generation and merit *source/patch-level* review **if** that kernel is loaded:

1. **CVE-2016-5195 (Dirty COW)** — local privilege escalation through the copy-on-write race. See https://nvd.nist.gov/vuln/detail/CVE-2016-5195 .
2. **CVE-2014-3153 (futex_requeue)** — local privilege escalation or denial of service in affected, unpatched kernels through version 3.14.5. See https://ubuntu.com/security/CVE-2014-3153 .

These are **candidates based on family and date, not confirmed vulnerabilities in Mini-Cam hardware**. The image may have vendor fixes, and the running kernel may differ. No exploit attempts, login attempts, or target scans have been made. A fourth owner's offline inventory notebook has been added, which lists files and selected configuration flags without reading customer records.

## Fourth Colab inventory: installed GUI runtimes and services (2026-11-05)

The owner's private `PX1_SD_INVENTORY_REPORT.txt` was read successfully. Selected technical evidence:

- `/usr/local/Trolltech` contains `Qtmobile-1.2.0-mx5x`, `Qt-4.7.4-mx5x-x11`, `Qt-4.7.2-mx5x-x11`, and `Qt-4.7.4-mx5x-x11-SAVED` directories. Multiple GUI/runtime versions coexist on the disk, but this **does not establish which one is used by the running application**.
- `/usr/local/sbin` contains `wpa_supplicant`, `wpa_passphrase` and `wpa_cli`: software for Wi-Fi configuration is present. This is **not proof that a Wi-Fi service is listening or reachable**.
- `/usr/local/bin` contains OpenCV sample/training executables and serial-transfer utilities `rz`, `rx`, `sz`, `sx`, `sb`, `rb`. Existence of these files is **not evidence the Mini-Cam app uses them**.
- `/etc/rc.d` includes `rc.conf`, `rc.serial`, `rc.modules`, `rcS`, `rc.local`, `init.d`, consistent with a traditional SysV-style embedded-Linux boot scheme. Scripts have not been read or executed.
- Image's `/boot/linux.config` contains `CONFIG_MODULES=y`, `CONFIG_INET=y`, `CONFIG_WIRELESS=y`, `CONFIG_USB_GADGET=y`. These describe a saved kernel *build configuration*, not verified active services.

### Additional candidates worth patch-level review

- **CVE-2011-3194**: TIFF image parsing overflow was reported for Qt 4.7.4. Directory names alone cannot show whether the bundled Qt libraries lack the correction or whether the affected TIFF handler is installed and used. Reference: https://security.gentoo.org/glsa/201206-02
- **CVE-2012-6093**: Qt 4.7.x before 4.7.6 may mishandle TLS certificate-validation errors **under particular OpenSSL ABI/version combinations**. This is a conditional candidate, not proof of exposure. Reference: https://nvd.nist.gov/vuln/detail/CVE-2012-6093
- **CVE-2015-1860**: affected pre-4.8.7 Qt GUI GIF parsing can overflow when processing crafted images; relevance depends on whether a vulnerable Qt image handler is present and unpatched and whether crafted GIFs can reach it. Vendor Qt advisory: https://lists.qt-project.org/pipermail/announce/2015-April/000067.html

**Finding status:** No exploitable issue has been demonstrated in Mini-Cam firmware; this is an **offline component inventory and version-screening**, not an active scan of Mini-Cam Ltd.
