# PX-1 Rev.R16 — CRP-150-style rebuild after user review

Status: **PASS_R16_NOMINAL_PACKAGING_STUDY**.  This is a nominal CAD gate,
not a machining, pressure, traction or IP-rating release.

## Что изменено по замечаниям

### Задняя часть

The pressure body ends at **X=307 mm**.  The only rigid rear extension is the
short axial connector/strain-relief stack to **X=320 mm**, centred at
**Z=58 mm**.  It is above the wheel contact plane and does not form a low hook.
The cable itself remains the existing flexible aramid-reinforced tether and is
not represented as a rigid tail.  The lowering/towing eye is integrated in the
rear cover, with its top at **Z=110 mm**.

### Колёса и колёсная база

The body side recess, side cover and wheel flanges are one structural wheel
station.  There is no detached wheelbase module.  Wheel centres are
**X=50/150/250 mm**, **Z=45 mm**; the 90 mm tread therefore reaches
**Z=0 mm** at all six stations.  The tire/hub service solids are separated so
the wheel can slide over the Ø35 mm flange after the retainer is released.

The body-plus-wheel envelope is **307 × 133 × 90 mm**.  The pressure body
itself is **307 × 92 × 82 mm**.  Rounded Y-Z lower corners keep the hard body
inside the ideal ID150 pipe; the wheel tread is the compliant pipe-contact
surface and still requires a physical DN150 sweep.

### Быстросъём колеса

The R15 M8/nut service path is removed.  Each station now has:

1. a keyed Ø17 wheel seat for torque;
2. a recessed captive retaining cap;
3. a Ø4.4 cross-drilled ball-lock pin with hand tabs;
4. a small lanyard eye so the pin/cap can remain captive.

The pin is axial-retention hardware only; it must not be used to transmit drive
torque.  The pin is pulled along the wheel's transverse X direction; after it
is released, the wheel slides outward along the side Y axis.  The CAD check
records six tool-free service locations.  Mud, ice,
corrosion and repeated pull testing remain mandatory before approving a
specific catalogue pin.

### Лифт и камера

The lift is moved to the body centreline/front-central zone at **X=150 mm**.
Two 80 mm links fold over the roof saddle in LOW and align vertically in HIGH;
the camera centre remains **X=150 mm** in both poses.  LOW camera centre is
**Z=119 mm** and the nominal raised centre is **Z=250 mm**.  A positive lock
sector and pin are modeled; the 150 N spring is only an installation envelope.

The old camera envelope is replaced by a separate **88 × 54 × 48 mm** rounded
armoured pod.  It has a recessed 27 mm optical opening, a mechanically retained
front guard ring, an internal elastomer-isolator envelope for the RunCam Phoenix
2 SE V2 board, and a keyed service interface with hand-release yoke pins.  The
pod nests in a 92 × 60 mm open roof pocket at LOW and has zero nominal volume
outside the ideal ID150 pipe in that pose.

### Силовая электроника внутри корпуса

The previous RSD-100D-24 reserve was not accepted: its 161 × 68 × 36 mm body
collided with the motor/driver reserve once the body was made CRP-150-like.
R16 uses a **Mean Well RSD-60H-24** candidate (128 × 60 × 25 mm, 60 W,
40…160 VDC input, 24 V/2.5 A nominal output) in the front dry bay.  The two
Pololu 4695 motor envelopes are staggered in X and the NUCLEO/DRV8871/SU-1P
envelopes are checked as separate, non-overlapping reserves.  This is a
packaging and power-budget candidate, not a thermal or electrical safety
release.

## CAD checks recorded

The generated `validation.json` records:

- all named solids valid;
- no hard housing/lift/rear part outside the ideal ID150 cylinder;
- all six wheels touch the Z=0 contact plane;
- 10 equal Z50 m1 gear envelopes per side (five per side);
- four 80 mm lift links in LOW/HIGH pose checks;
- zero nominal camera-pod/saddle and lift-link/camera collisions;
- six hand-accessible wheel retainers;
- body-plus-wheel width exactly 133 mm.
- body electronics reserve boxes stay inside the 287 × 72 × 66 mm dry envelope
  without nominal overlaps.

Wheel/shaft/retainer intersection volumes are intentionally kept as an
**advisory** in the report because the wheel tread is the compliant pipe
contact and the hub/shaft are internal service geometry.  This is not a claim
that the real wheel will clear every oval, deposit or bend.

## Что ещё нельзя утверждать по одному CAD

- герметичность/IP68 или удержание +1 bar;
- тягу на мокрой трубе, зацепление шестерён под нагрузкой;
- прочность 3D-печатной детали или алюминиевого корпуса;
- фактическую жёсткость/нагрузку ручного лифта;
- то, что конкретный RunCam объектив и выбранное окно без измерения войдут в
  pod;
- то, что любой найденный ball-lock pin выдержит удар и многократный съём.

Before machining, measure the purchased bearings, X-rings, wheel, flange and
pin; make one wheel-station coupon; prove the pod with the real lens/window;
then pressure-test and run the complete robot in an actual ID150 tube.
