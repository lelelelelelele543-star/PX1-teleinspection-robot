"""Rebuild and export R16 for visual review, including a failed pipe-fit audit.

Never treat a successful file export as successful engineering validation.
"""
from pathlib import Path
import hashlib
import json
import math
import shutil
import sys
import zipfile

import cadquery as cq
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import PX1_R16_ProteusRebuild as r16

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
BUILD = ROOT / 'build_r16_review_20260910'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def log(message):
    print(message, flush=True)


reuse = '--reuse' in sys.argv[2:]
if reuse:
    log('Reusing the current-source CAD build and completed validation')
    index = json.loads((BUILD/'named_parts/index.json').read_text())
    assert index['source_sha256'] == sha(Path(r16.__file__))
    parts = {n: cq.Workplane('XY').newObject([cq.Shape.importBrep(str(BUILD/'named_parts'/f))])
             for n,f in index['files'].items()}
    groups = index['groups']
    report = json.loads((BUILD/'validation.json').read_text())
else:
    log('Building current R16 geometry')
    parts, groups = r16.build_parts()
    log(f'Built {len(parts)} named parts; running corrected pipe-fit check')
    report = r16.validate(parts, groups, BUILD)
assert report['status'] == 'FAIL_R16_NOMINAL_PACKAGING'
assert report['pipe_outside_mm3']['Wheel_L_50'] > 50000
assert report['pipe_outside_mm3']['Axle_L_50'] > 1
log('Engineering status: FAIL; exporting review geometry only')
if not reuse:
    r16.export(parts, groups, BUILD)
step = OUT / 'PX1_R16_REVIEW.step'
shutil.copyfile(BUILD / 'PX1_R16_ASSEMBLY.step', step)

# Round-trip confirms an intact transfer, independent of the engineering gate.
expected_count = sum(len(r16.solids(p)) for p in parts.values())
negative_orientations = [n for n,p in parts.items()
                         if any(s.Volume()<0 for s in r16.solids(p))]
# STEP canonicalizes solid orientation. Compare occupied volume, retaining
# evidence of the source's three reversed right-hub solids in the audit.
expected_volume = sum(abs(s.Volume()) for p in parts.values() for s in r16.solids(p))
receipt_path = BUILD/'step_roundtrip.json'
if reuse and receipt_path.exists():
    receipt = json.loads(receipt_path.read_text())
    assert receipt['step_sha256'] == sha(step)
else:
    log('Reopening STEP to verify solids and volume')
    imported = cq.importers.importStep(str(step)).solids().vals()
    receipt = {'step_sha256':sha(step),'solid_count':len(imported),
               'all_solids_valid':all(s.isValid() for s in imported),
               'import_volume_mm3':sum(s.Volume() for s in imported)}
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
volume_error = abs(receipt['import_volume_mm3']-expected_volume)
assert receipt['solid_count'] == expected_count
assert receipt['all_solids_valid']
assert volume_error < .01

# A single explicit point proves the stated flat-ground placement impossible
# in the cylinder, regardless of meshing or tyre/contact assumptions.
y = 60.25
z = 45.0 - 39.5
pipe_floor = 75.0 - math.sqrt(75.0**2 - y**2)
audit = {
    'engineering_status': report['status'],
    'manufacturing_release': False,
    'dn150_fit_verified': False,
    'source_sha256': sha(Path(r16.__file__)),
    'step_sha256': sha(step),
    'step_import_solids': receipt['solid_count'],
    'step_solids_valid': True,
    'step_volume_error_mm3': volume_error,
    'source_negative_solid_orientations_normalized_by_STEP': negative_orientations,
    'counterexample': {
        'wheel_point_yz_mm': [y, z],
        'pipe_floor_at_same_y_mm': pipe_floor,
        'minimum_upward_shift_to_clear_this_point_mm': pipe_floor-z,
        'camera_guard_top_after_that_shift_mm': 147.0+pipe_floor-z,
        'pipe_top_mm': 150.0,
        'meaning': 'A vertical lift of the whole current assembly cannot fix this fit.'
    },
    'wheel_station_outside_mm3': report['wheel_service_pipe_intersection_advisory_mm3'],
}
(OUT / 'R16_REVIEW_AUDIT.json').write_text(json.dumps(audit, indent=2)+'\n')
(ROOT / 'validation/r16/delivery_audit.json').write_text(json.dumps(audit, indent=2)+'\n')
shutil.copyfile(BUILD / 'validation.json', ROOT / 'validation/r16/validation.json')

log('Rendering the actual CAD geometry')
meshes = []
for name, p in parts.items():
    if groups[name] in ('internal_reserve', 'drive', 'seal_interface'):
        continue
    verts, faces = p.val().tessellate(.35, .3)
    vertices = np.array([[v.x, v.y, v.z] for v in verts])
    tri = vertices[np.array(faces)]
    if name.startswith('Wheel_'):
        color = '#232c34'
    elif 'CameraWindow' in name:
        color = '#44a2bf'
    elif 'Camera' in name:
        color = '#334b5d'
    elif 'Lift' in name or 'GasSpring' in name:
        color = '#d39942'
    elif 'QuickRelease' in name:
        color = '#b37d31'
    else:
        color = '#b6bec5'
    meshes.append((tri, color))

fig = plt.figure(figsize=(15, 8.4), dpi=160, facecolor='#f5f6f7')
fig.text(.045, .94, 'PX1 / R16', fontsize=26, weight='bold', color='#243443')
fig.text(.045, .905, 'Текущая CAD-компоновка для просмотра', fontsize=14, color='#546372')
all_triangles=np.concatenate([tri for tri,color in meshes])
all_colors=np.concatenate([np.tile(to_rgba(color),(len(tri),1)) for tri,color in meshes])
for rect, elev, azim, title in [([.02,.39,.60,.49],24,-136,'Общий вид'),
                                ([.60,.39,.38,.49],0,-90,'Вид сбоку')]:
    ax=fig.add_axes(rect, projection='3d', facecolor='#f5f6f7')
    # Sort all triangles together: per-part average depth can incorrectly
    # draw the large pressure body in front of the nearer wheels.
    ax.add_collection3d(Poly3DCollection(all_triangles,facecolors=all_colors,
                                       linewidths=0,shade=True,zsort='average'))
    ax.set(xlim=(-12,332),ylim=(-78,78),zlim=(0,163))
    ax.set_box_aspect((344,156,163))
    ax.view_init(elev=elev,azim=azim)
    ax.set_proj_type('ortho')
    ax.set_axis_off()
    ax.set_title(title,fontsize=12,color='#546372',y=.94)

ax=fig.add_axes([.065,.065,.25,.28],facecolor='#f5f6f7')
theta=np.linspace(0,2*math.pi,600)
ax.plot(75*np.cos(theta),75+75*np.sin(theta),color='#778898',linewidth=2)
ys=np.array([51.25,53.25,56.25,60.25,63.75,66.5])
rs=np.array([45,45,44,39.5,31,18.5])
for side in (1,-1):
    ax.fill(np.r_[side*ys,side*ys[::-1]],np.r_[45-rs,45+rs[::-1]],
            color='#303d48',alpha=.85)
ax.scatter([y],[z],s=28,color='#c74636',zorder=4)
ax.plot([y,y],[z,pipe_floor],color='#c74636',linewidth=2)
ax.set(xlim=(-82,82),ylim=(-6,156),aspect='equal')
ax.set_title('Колёса в сечении трубы Ø150',fontsize=10,color='#546372')
ax.set_axis_off()
fig.text(.34,.305,'Ø150: обнаружено пересечение',fontsize=17,weight='bold',color='#b44133')
fig.text(.34,.255,'В прежнем PASS колёса и ступицы были исключены.',fontsize=12,color='#243443')
fig.text(.34,.212,f'В показанной точке колесу не хватает {pipe_floor-z:.1f} мм по высоте.',fontsize=12,color='#243443')
fig.text(.34,.169,'Поднять весь робот нельзя: камера выйдет за верх трубы.',fontsize=12,color='#243443')
fig.text(.34,.102,'Нужна переработка профиля колёс и высоты сложенной камеры.',fontsize=11,color='#546372')
fig.text(.34,.062,'R16 не утверждена для изготовления. Масштабы видов различаются.',fontsize=10,color='#546372')
png=OUT / 'PX1_R16_REVIEW.png'
fig.savefig(png,facecolor=fig.get_facecolor())
plt.close(fig)

readme='''PX1 R16 — модель для просмотра, не для изготовления

Открыть PX1_R16_REVIEW.step в FreeCAD: Файл → Открыть.
Единицы — миллиметры. STEP сохраняет отдельные тела, но не историю эскизов.
Источник программы: https://www.freecad.org/

Прилагается текущая R16 после замечаний к R15. Это НЕ завершённая конструкция.
Корпус: 307 × 92 × 82 мм. Корпус с колёсами: 307 × 133 × 90 мм.
Общая модель с камерой и хвостовым интерфейсом: 320 × 133 × 147 мм.

10.09.2026: прежний PASS отозван. Колёса, ступицы и концы валов пересекают
стенку идеальной трубы ID150 в показанном положении. Контакт колёс с плоскостью
Z=0 не подтверждает размещение в круглой трубе. Для одной точки колеса требуется
подъём на 24,835 мм, после которого верх камеры оказывается выше трубы.
Текущая проверка правильно возвращает FAIL_R16_NOMINAL_PACKAGING.

Модель служит для обсуждения внешней формы. Внутренние модули показаны
габаритами; полной рабочей связи моторов с передачами и полной проверки
пересечений всех деталей здесь нет. Быстросъём представлен концепцией без
утверждённого покупного фиксатора. Приводы камеры не получили герметичных
кожухов. Уплотнения, крепления и сборочные допуски не готовы к изготовлению.

R16_REVIEW_AUDIT.json — независимая контрольная точка и проверка STEP.
checks/validation.json — актуальный отрицательный результат проверки.
source/ — исходники текущей компоновки с исправленным критерием допуска.
PX1_R16_REVIEW.png — изображение из геометрии CAD, без генеративной дорисовки.
'''
(OUT / 'READ_ME_R16_RU.txt').write_text(readme,encoding='utf-8')
archive=OUT / 'PX1_R16_REVIEW.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zf:
    for p in [step,png,OUT/'READ_ME_R16_RU.txt',OUT/'R16_REVIEW_AUDIT.json']:
        zf.write(p,p.name)
    zf.write(BUILD/'validation.json','checks/validation.json')
    zf.write(Path(r16.__file__),'source/PX1_R16_ProteusRebuild.py')
    zf.write(Path(__file__),'source/export_r16_review_pack.py')
    zf.write(ROOT/'mechanical/cadquery/requirements-r16.txt','source/requirements-r16.txt')
with zipfile.ZipFile(archive) as zf:
    assert zf.testzip() is None
log(json.dumps({'status':'REVIEW_EXPORT_READY_ENGINEERING_FAIL',
                'files':[str(step),str(png),str(archive)],
                'solid_count':receipt['solid_count'],'volume_error_mm3':volume_error,
                'counterexample':audit['counterexample']},ensure_ascii=False))
