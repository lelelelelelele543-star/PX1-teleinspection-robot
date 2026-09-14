# PX-1 pressure fill / purge adapter — Rev.B WB24A

Date: 2026-09-14
Status: **SERVICE TOOL PROTOTYPE / THREAD + STROKE HOLD**

The adapter is a removable workshop/field tool. It is never installed while driving the crawler and therefore does not belong to the DN150 moving envelope.

## Purpose

One tool must allow the technician to:

- screw onto/into the low-profile PX1 PRESSURE port after removing the protection cap;
- mechanically open the internal valve positively;
- connect a regulated air / CO2 / nitrogen source;
- monitor pressure through the crawler pressure sensor/control display;
- purge pressure back to ambient before opening the service cover.

This follows the documented Proteus operating logic: remove protection cap, screw on pressure adaptor, fill, remove adaptor, refit cap. A purge screw is also documented on the Proteus Ex pressure-valve tool.

## Prototype interface

Crawler-side thread candidate:

- `M8 x 1` male nose on adapter;
- engagement target around 4–5 mm;
- thread remains prototype only until the actual valve stack is bench-tested.

Opening probe:

- central stainless probe;
- adjustable effective protrusion by replaceable shim/stop during first bench development;
- prototype opening stroke target only ~0.5...1.0 mm;
- rounded probe end; no sharp point against valve shaft/ball;
- positive shoulder prevents over-stroking the internal valve.

Gas passage:

- axial bore around/through probe arrangement;
- cross drillings downstream of thread seal so gas reaches valve mouth even while the probe is depressing the check element;
- passage >=1.5 mm class is ample for the small crawler volume and low fill pressure; exact drill is not performance-critical.

## Tool-side connection

Do not hard-code the crawler to one compressor fitting.

Adapter body ends in a standard replaceable pneumatic interface. Prototype choices:

- G1/8 female port plus interchangeable hose nipple/quick coupling; or
- G1/8 port plus a separate tire-chuck/Schrader tool fitting if the user's compressor gun is a tyre inflator.

This keeps all bulky marketplace pneumatic hardware on the removable service tool rather than on the crawler roof.

## Purge function

Preferred adapter includes a small needle/purge screw:

- positioned downstream of the crawler valve so opening it vents crawler pressure while adapter remains screwed in and valve remains mechanically open;
- screw cannot fall out in normal use;
- vent direction points away from the operator's face;
- flow is deliberately modest so pressure can be watched on the control unit while venting.

A simple M4-class needle screw is a prototype concept only; final seat/O-ring/thread geometry follows the actual machined tool.

## Operating sequence

1. crawler OFF for mechanical service, or powered only as required to read pressure safely;
2. clean valve area;
3. unscrew low-profile protection cap;
4. screw WB24A adapter into pressure port until shoulder seats — do not overtighten;
5. close purge screw;
6. connect regulated source;
7. set source regulator to a safe low pressure; never connect bottle/compressor reservoir directly without regulation;
8. fill while watching crawler pressure reading;
9. isolate source;
10. disconnect source hose if desired;
11. for normal operation, unscrew adapter and confirm valve closes without bubbling/leak indication;
12. reinstall clean protection cap.

For depressurisation before service:

1. screw adapter in so valve is mechanically opened;
2. open purge screw slowly;
3. watch pressure fall to ambient;
4. only then loosen the PRESSURE/CAMERA SERVICE cover.

## Safety rule

The adapter is not a pressure regulator. The source must be regulated upstream.

PX1 normal development pressure remains approximately +0.25 bar gauge unless a later controlled pressure specification supersedes it. The service tool should be rated comfortably above the test/proof pressure, but high tool rating does not authorize over-pressurising the crawler.

## Prototype drawings to make after valve bench test

After the winning WB24A valve insert is known, release:

- ADP-PX1-001 adapter body;
- ADP-PX1-002 opening probe;
- ADP-PX1-003 purge screw;
- tool-side G1/8 fitting callout;
- probe-stroke gauge/check dimension.

The adapter must be tested together with the valve; neither is independently released.
