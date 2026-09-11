# PX-1 Rev.B — WB14 exact camera / fixed-shell illumination

Date: 2026-09-11
Status: CAMERA BASELINE RETAINED / LIGHTING ARCHITECTURE FROZEN / OPTICS+THERMAL QUALIFICATION HOLD

## 1. Architecture check before component change

No justified reason was found to replace the existing compact RunCam camera baseline.

Earlier Rev.BI already selected `RunCam Phoenix 2` because it is much smaller than ordinary 32/34 mm CCTV boards while preserving analog CVBS. A WB14 sourcing exploration briefly considered a 34 mm-class CCTV module. That would have increased the camera envelope without solving a demonstrated failure and is therefore rejected.

Decision:
- preserve RunCam Phoenix 2 family;
- do not redesign the Ø52 head around a larger board camera;
- qualify lens/FOV independently because the stock 2.1 mm wide-angle lens is the real optical open item.

## 2. Selected camera baseline

### RunCam Phoenix 2

Controlled manufacturer data for the standard Phoenix 2:
- SKU family: `PHOENIX2-SL`;
- image sensor: 1/2 in CMOS;
- analog output: PAL / NTSC switchable CVBS class;
- horizontal resolution: 1000 TVL;
- stock lens: 2.1 mm, M12, FOV about 155 deg in 4:3;
- supply: 5...36 VDC;
- current: current manufacturer page lists ~85 mA at 12 V; older manual revision lists ~120 mA at 12 V;
- design power reservation: use the higher 120 mA value until the purchased sample is measured;
- nominal current-product dimensions: 19 x 19 x 19 mm; older manual shows about 19 x 19 x 20 mm;
- mass: ~9 g.

Rev.B CAD/service envelope remains:
- 20 x 20 x 22 mm around the purchased camera body, excluding the final lens projection;
- M2 mounting points verified from the purchased sample before machining the carrier;
- at least 0.5 mm assembly clearance around the ABS camera body and >=1 mm preferred where wire bend permits.

### Procurement

An AliExpress marketplace route for the standard Phoenix 2 is currently indexed, including RunCam Official Store / established FPV sellers. Exact listing and seller stock must be rechecked on purchase day.

A current Czech retail alternative `Phoenix 2 SE V2` also exists at 19 x 19 x 22 mm, 5...36 V, ~80 mA at 12 V. It is a supply fallback, not an automatic geometry change.

The first purchased camera must be photographed, measured and electrically characterized before the camera carrier drawing is released.

## 3. Camera video-output qualification

Do not invent a 1 Vpp/75 ohm result from the FPV product category.

Before WB12 video-link release:
1. set camera to PAL for the first European/CVBS prototype;
2. terminate video into a real 75 ohm test load;
3. measure composite amplitude and sync tip with an oscilloscope;
4. record current at 12 V;
5. verify video return conductor is separate from the LED/motor high-current return in the head harness;
6. repeat through camera slip ring and Delta-Opti balun.

## 4. Lens/FOV correction

The standard 2.1 mm lens gives about 155 deg FOV. That is intentionally left usable for the first image test, but it is not frozen as the final sewer-inspection optic because:
- very wide optics increase barrel distortion;
- the front bezel/LED annulus is more likely to enter the image;
- useful forward detail at distance may be worse than a ~70-90 deg class lens.

The RunCam body uses an M12 lens mount, so the correct response is to test lenses before replacing the whole camera.

### Optical reference target
A commercially documented 5 mm M12 lens for a 1/2 in sensor exists with approximately:
- 5 mm focal length;
- M12 mount;
- 1/2 in compatibility;
- ~75.5 deg horizontal FOV;
- ~99 deg diagonal FOV;
- ~17 mm OD x 24 mm length class.

This geometry is an **optical engineering reference**, not a PX-1 procurement freeze because the currently verified source is outside the normal ChipDip/marketplace procurement rule.

Rev.B purchase sequence:
- test the stock RunCam 2.1 mm lens first;
- then buy a marketplace M12 lens only if its controlled image circle/BFL are compatible with the 1/2 in RunCam sensor;
- do not buy a 1/2.5 in-only lens and assume it will cover the larger 1/2 in sensor without vignetting;
- final FOV is selected from real pipe footage at roughly 150/200/300 mm pipe classes.

## 5. Important lighting geometry correction

The old idea of using six ready Ø16 mm XP-G star boards around the current Ø28 mm optical window is geometrically impossible inside a Ø52 mm head.

Minimum radial requirement for one Ø16 board around a Ø28 window is:
- window radius 14 mm;
- board radius 8 mm;
- centre radius must be >=22 mm;
- board outside radius then becomes >=30 mm;
- required ring diameter >=60 mm > 52 mm head OD.

Therefore Ø16 star modules are rejected for the final front annulus even though they are easy to buy.

## 6. Rev.B LED carrier

Keep the already selected Cree XP-family emitter concept, but mount each emitter on a **standard small commercial MCPCB**, not a custom camera PCB.

Preferred mechanical format:
- six individual 8 mm-class 3535/XP-G compatible aluminium MCPCBs;
- six centres on PCD 40 mm (R20);
- optical window: Ø28 mm;
- head OD: Ø52 mm.

Worst-case 8 x 8 mm square-board screen at R20:
- innermost board corner radius ~16.49 mm -> ~2.49 mm radial clearance to the Ø28 window;
- outermost board corner radius ~24.33 mm -> ~1.67 mm radial clearance to Ø52 head OD;
- adjacent centre spacing = 20 mm, leaving large inter-board wiring clearance.

This is an analytical packaging PASS for the board footprints only. Front-retainer fasteners, window O-ring groove and actual board thickness still require CAD integration.

### Source path

Marketplace suppliers currently offer 8/10/12/14/16/20 mm 3535 aluminium boards compatible with Cree XP-E/XT-E/XP-G family, and current marketplace listings exist for XP-G3 white emitters pre-mounted on sizes including 8 mm.

Final production emitter target remains the controlled Cree XP-G/XP-G3 white family previously selected by the project. Marketplace pre-mounted emitters are prototype/test articles unless their exact Cree order code/bin is traceable.

## 7. LED thermal mounting

The six MCPCBs are not glued permanently into the pressure shell.

Mechanical concept:
- fixed aluminium front LED carrier integrated with the static outer shell/front bezel;
- six shallow 8.2 mm-class seating pockets around PCD40;
- actual pocket depth follows the purchased MCPCB thickness;
- thin thermal compound or qualified thin thermal interface material under each MCPCB;
- one removable blackened retaining ring mechanically clamps the six boards;
- retaining ring also provides an optical black barrier between LEDs and the Ø28 window;
- no LED board becomes a pressure seal.

Service sequence:
1. remove front bezel/retainer;
2. remove optical separator/LED clamp ring;
3. desolder service leads;
4. replace one individual LED/MCPCB;
5. renew thermal compound;
6. reassemble and leak-test the unchanged window seal boundary.

## 8. LED electrical topology

### Preferred Rev.B topology
Use two independent strings:
- String A: 3 LEDs in series;
- String B: 3 LEDs in series;
- one ready P4115adj constant-current module per string.

Reason for two channels:
- one failed LED/string still leaves approximately half illumination;
- current can be matched during bench setup;
- modules are cheap and separately replaceable;
- no custom PCB is required.

### Ready driver
Prototype article:
- `P4115adj` ready module;
- PT4115-based step-down constant-current source;
- input 6...30 VDC, max 32 V according current module listing;
- guaranteed adjustment ranges ~200...400 mA with current-range bridge open and ~400...700 mA with bridge closed;
- PWM/DIM input accepts TTL ~2.5...5.5 V;
- max PWM class 50 kHz;
- minimum input-output headroom specified around 2 V;
- PCB ~29.3 x 15.1 mm, height ~9 mm;
- short-circuit and thermal protection stated by module maker;
- no reverse-input protection;
- active marketplace listing exists.

Quantity:
- 2 working modules;
- 1 spare recommended.

Initial current setting:
- bridge OPEN;
- set each channel to ~300 mA using an ammeter and dummy/real LED string;
- do not start at 700 mA.

This keeps heat and glare low while retaining large light reserve from six XP-class emitters.

## 9. 12 V dropout gate

The current camera-head service architecture provides a 12 V rail.

Three white XP-family LEDs in series are expected to be workable at ~300 mA, but the P4115adj module requires approximately 2 V of input/output margin.

Therefore final release is conditional on the actual purchased LED string voltage:
- measure each three-LED string at 300 mA cold and hot;
- require `12V_MIN - Vf_string >= 2.0 V` with useful supply tolerance;
- if this cannot be met, do NOT simply increase supply or overdrive the module.

Controlled fallback order:
1. choose verified lower-Vf Cree XP-family emitters/bins;
2. move the LED drivers to a qualified 24 V fixed-side supply while preserving two independent strings and camera-head serviceability;
3. only if wiring/connector packaging prevents that, review a different ready constant-current driver.

No custom boost PCB is introduced merely to save an unsuitable LED string.

## 10. PWM control

Both P4115adj DIM inputs receive the same light-level PWM command.

Starting electrical rule:
- one separate series resistor (~1 kOhm class) into each DIM lead;
- common driver input ground and MCU PWM reference as required by the module;
- 3.3 V STM32/RP2040-class PWM lies inside the module's stated TTL control range;
- default on MCU reset is LIGHT OFF through a hardware pulldown at DIM.

Exact PWM frequency starts in the low-kHz range, then is moved if video testing shows beat/noise artifacts. Do not operate near the camera line/frame frequencies without a noise test.

## 11. Fixed-shell lighting — slip-ring correction

The active mechanical head architecture places the LED annulus on the **fixed outer shell**. Continuous ROLL occurs only in the inner camera carrier.

Therefore:
- LED power does NOT pass through the camera ROLL slip ring;
- LED PWM does NOT pass through the ROLL slip ring;
- TILT/ROLL motor power does not need to pass through that slip ring if motors/drivers remain fixed-side;
- the rotating interface carries only the functions required by the rotating camera sensor itself.

This corrects WB13's conservative assumption that PAN/light current travelled through the camera slip ring.

## 12. Thermal budget

Starting lighting point at 300 mA:
- six LEDs, approximate electrical input of ~0.85...1.05 W each depending real Vf;
- LED electrical total ~5.1...6.3 W class;
- driver losses additional but modest when adequate headroom is maintained;
- camera itself reserves ~1.4 W at the conservative 12 V / 120 mA design value.

The fixed aluminium LED carrier must conduct LED heat to the outer shell.

Qualification:
- still-air dry test first;
- submerged/wet shell test second;
- full-light 30 min soak while camera runs;
- record LED-carrier, driver, camera-case and internal-air temperatures;
- repeat with one driver/string disabled to verify service/fault behavior.

## 13. Mechanical architecture correction — no cartridge/cassette

Older `REV_BU` / `REV_FA` text used `internal roll cartridge` language. That conflicts with the current project prohibition on cartridge/cassette mechanical modules.

Rev.B interpretation is now:
- static sealed outer shell;
- ordinary integrated inner ROLL carrier/spindle;
- two serviceable bearings;
- ordinary shaft/gear/retainers;
- removable front/rear covers;
- no self-contained removable cartridge/cassette.

Also, `REV_FA` contains an obsolete digital/Ethernet camera path and is historical wherever it conflicts with active CVBS Rev.B documents.

## 14. WB14 release gates

Before production drawing release:
1. buy and measure exact RunCam Phoenix 2 sample;
2. measure CVBS into 75 ohm and camera current at 12 V;
3. inspect stock 2.1 mm image in real pipe;
4. decide whether a ~5 mm / ~75 deg-class M12 lens is actually needed;
5. buy six 8 mm-class XP-family LED assemblies/MCPCBs and measure thickness/Vf;
6. buy two P4115adj modules and characterize current/dropout/PWM;
7. integrate six LED footprints, window O-ring, separator and fasteners in front-head CAD;
8. physically prove two-driver placement in the fixed head/cradle zone;
9. 30 min full-light thermal test;
10. run WB12 video-noise test with LED PWM from 0...100%;
11. only then freeze front-ring pocket depth, wire routing and production lens.

## Change log

### 2026-09-11 — WB14
- preserved RunCam Phoenix 2 instead of needlessly changing to a larger CCTV camera;
- updated the camera electrical envelope from current manufacturer data while retaining the conservative 120 mA design reservation;
- left final M12 focal length measurement-driven;
- rejected six Ø16 star boards as geometrically impossible around the Ø28 window inside Ø52;
- selected six 8 mm-class standard MCPCB footprints on PCD40;
- selected two ready P4115adj channels at ~300 mA initial setting for lighting redundancy;
- established the 12 V LED-string dropout test;
- corrected the camera slip-ring load by keeping fixed-shell LEDs off the rotary interface;
- formally removed old cartridge/cassette and digital-camera concepts from the active Rev.B interpretation.
