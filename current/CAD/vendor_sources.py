"""Download the exact publicly published vendor STEP resources; do not scale."""
from pathlib import Path
import urllib.request,zipfile,io,hashlib,json
root=Path(__file__).resolve().parent
vendor=root/'vendor';vendor.mkdir(exist_ok=True)
sources={}
def fetch(url,name):
    out=vendor/name
    if not out.exists():
        with urllib.request.urlopen(url,timeout=90) as r:out.write_bytes(r.read())
    sources[name]={'url':url,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
url='https://www.pololu.com/file/0J1113/25d-gearmotor-3d-models.zip'
name='Pololu_25D_75_99_Manufacturer.step';out=vendor/name
if not out.exists():
    with urllib.request.urlopen(url,timeout=90) as r:z=zipfile.ZipFile(io.BytesIO(r.read()))
    matches=[n for n in z.namelist() if n.lower().endswith('25d-metal-gearmotor-75-99.step')]
    assert len(matches)==1,matches
    out.write_bytes(z.read(matches[0]))
sources[name]={'url':url,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
fetch('https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32F4_64Pin_CoreBoard/master/Hardware/WeAct-STM32F4_64PIN-CoreBoard_V11%203D.step','WeAct_F4_64Pin_V11_Manufacturer.step')
fetch('https://www.pololu.com/file/0J1330/g2-high-power-motor-driver-md31a.step','Pololu_G2_24v13_Manufacturer.step')
(vendor/'SOURCE_HASHES.json').write_text(json.dumps(sources,indent=2))
print('Vendor files ready',len(sources),flush=True)
