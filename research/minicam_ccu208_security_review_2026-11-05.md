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
