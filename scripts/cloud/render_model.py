#!/usr/bin/env python3
"""Render the master assembly's actual tessellated surfaces, without a display.

Usage: python scripts/cloud/render_model.py BUILD_DIRECTORY
Requires numpy, Pillow and a C compiler (cc). A tiny temporary C rasterizer uses
an orthographic projection and a per-pixel depth buffer. No CAD geometry is
redrawn, simplified, filled from bounding boxes, or generated from a prompt.
The source tessellation tolerances are recorded by release_tools.py.
"""
from pathlib import Path
import argparse
import ctypes
import gzip
import hashlib
import json
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RASTER_C = r'''
#include <math.h>
#include <stddef.h>
void raster(const double *tri, const unsigned char *col, size_t count,
            int w, int h, double *depth, unsigned char *rgb) {
  for (size_t i=0;i<count;i++) {
    const double *p=tri+9*i;
    double ax=p[0], ay=p[1], bx=p[3], by=p[4], cx=p[6], cy=p[7];
    double area=(bx-ax)*(cy-ay)-(by-ay)*(cx-ax);
    if (fabs(area)<1.e-9) continue;
    int x0=(int)floor(fmin(ax,fmin(bx,cx))), x1=(int)ceil(fmax(ax,fmax(bx,cx)));
    int y0=(int)floor(fmin(ay,fmin(by,cy))), y1=(int)ceil(fmax(ay,fmax(by,cy)));
    if(x0<0)x0=0; if(y0<0)y0=0; if(x1>=w)x1=w-1; if(y1>=h)y1=h-1;
    for(int y=y0;y<=y1;y++) for(int x=x0;x<=x1;x++) {
      double px=x+.5, py=y+.5;
      double b=((px-ax)*(cy-ay)-(py-ay)*(cx-ax))/area;
      double c=((bx-ax)*(py-ay)-(by-ay)*(px-ax))/area;
      double a=1.-b-c;
      if(a<0 || b<0 || c<0)continue;
      double z=a*p[2]+b*p[5]+c*p[8]; size_t k=(size_t)y*w+x;
      if(z>depth[k]){depth[k]=z;rgb[3*k]=col[3*i];rgb[3*k+1]=col[3*i+1];rgb[3*k+2]=col[3*i+2];}
    }
  }
}
'''


def font(size):
    for path in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                 '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf'):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def drivetrain(item):
    name, category = item['id'], item['category']
    if 'GAS_SPRING_CLEVIS_PIN' in name:
        return False  # belongs to the hidden lift, not the drivetrain
    return category in {'gear', 'bevel', 'shaft', 'bearing', 'seal'} or any(
        token in name for token in ('TRACTION_MOTOR_', 'POLOLU_5707_MOTOR_', 'NBK_MLR', 'PAIRED_MOTOR_HOLDER',
                                   'PAIRED_PINION_BEARING_HOLDER', 'AXLE_FLANGE'))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    out = args.output.resolve()
    mesh_path = out / 'images' / 'assembly_mesh.json.gz'
    with gzip.open(mesh_path, 'rt') as stream:
        meshes = json.load(stream)
    validation = json.loads((out / 'PX1_Current_Validation.json').read_text())
    compiler = shutil.which('cc')
    if not compiler:
        raise SystemExit('A C compiler (cc) is needed for the headless depth-buffer renderer.')
    pipe_z=validation['dn150']['assumed_pipe_center_z_mm']
    pipe_r=validation['dn150']['diameter_mm']/2
    views = [
        ('isometric', 'PX1 | Integrated six-wheel assembly', (-.7, -1., .65), lambda _: True,
         'All components shown; opaque CAD surfaces.'),
        ('side', 'PX1 | Side view', (0., -1., 0.), lambda _: True,
         'All components shown; opposite-side parts may be occluded.'),
        ('pipe', 'PX1 | Nominal DN150 contact pose', (-1.,0.,0.), lambda _: True,
         'Actual CAD front projection; engineered tyre profile, nominal ID150 circle. Physical fit NOT qualified.'),
        ('drivetrain', 'PX1 | Drivetrain inspection view', (-.45, -1., .95), drivetrain,
         'Hidden: body, covers, tyres, camera, lift, electronics and harnesses. Not a section cut.'),
    ]
    w, h = 1800, 1000
    manifest = {'mesh_sha256': hashlib.sha256(mesh_path.read_bytes()).hexdigest(),
                'source_sha256': validation['source_sha256'],
                'renderer': 'orthographic triangle rasterization, per-pixel z buffer',
                'manufacturing_release': False, 'views': []}
    with tempfile.TemporaryDirectory(prefix='px1-render-') as tmp:
        src, lib = Path(tmp) / 'raster.c', Path(tmp) / 'raster.so'
        src.write_text(RASTER_C)
        subprocess.run([compiler, '-O3', '-shared', '-fPIC', str(src), '-o', str(lib), '-lm'], check=True)
        raster = ctypes.CDLL(str(lib)).raster
        raster.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t,
                           ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        raster.restype = None
        for key, title, direction, include, note in views:
            shown = [item for item in meshes if include(item)]
            direction = np.asarray(direction, dtype=float)
            direction /= np.linalg.norm(direction)
            right = np.cross([0., 0., 1.], direction)
            right /= np.linalg.norm(right)
            up = np.cross(direction, right)
            basis = np.array([right, -up, direction]).T
            vertices = [np.asarray(item['vertices'], dtype=float) @ basis for item in shown]
            bounds = np.vstack([(v.min(axis=0), v.max(axis=0)) for v in vertices])
            if key=='pipe':
                pipe_extrema=np.asarray([(0,-pipe_r,pipe_z),(0,pipe_r,pipe_z),(0,0,pipe_z-pipe_r),(0,0,pipe_z+pipe_r)])@basis
                bounds=np.vstack([bounds,pipe_extrema])
            low, high = bounds.min(axis=0), bounds.max(axis=0)
            scale = min((w-140)/(high[0]-low[0]), (h-280)/(high[1]-low[1]))
            center = (low + high)/2
            rgb = np.full((h,w,3), (237,241,245), dtype=np.uint8)
            depth = np.full((h,w), -np.inf, dtype=np.float64)
            count = 0
            light = np.array([-.3,-.5,1.]); light /= np.linalg.norm(light)
            for item, projected in zip(shown, vertices):
                faces = np.asarray(item['triangles'], dtype=np.int64)
                raw = np.asarray(item['vertices'], dtype=float)[faces]
                normals = np.cross(raw[:,1]-raw[:,0], raw[:,2]-raw[:,0])
                norms = np.linalg.norm(normals, axis=1)
                normals /= np.maximum(norms[:,None], 1e-15)
                # Two-sided shading: CAD tessellation can include reversed shells.
                shade = .40 + .60*np.abs(normals @ light)
                color = np.asarray(item['color'], dtype=float)
                colors = np.ascontiguousarray(np.clip(shade[:,None]*color*255, 0,255), dtype=np.uint8)
                screen = projected.copy()
                screen[:,:2] = (screen[:,:2]-center[:2])*scale + [w/2,h/2+20]
                triangles = np.ascontiguousarray(screen[faces], dtype=np.float64)
                raster(triangles.ctypes.data, colors.ctypes.data, len(faces), w,h,
                       depth.ctypes.data,rgb.ctypes.data)
                count += len(faces)
            im = Image.fromarray(rgb)
            draw = ImageDraw.Draw(im)
            if key=='pipe':
                pc=np.asarray([0.,0.,pipe_z])@basis
                pc=(pc[:2]-center[:2])*scale+np.array([w/2,h/2+20])
                rr=pipe_r*scale
                draw.ellipse((pc[0]-rr,pc[1]-rr,pc[0]+rr,pc[1]+rr),outline='#16758d',width=3)
            draw.text((48,28), title, font=font(32), fill='#172c40')
            draw.text((48,77), note, font=font(20), fill='#40556a')
            draw.line((48,115,w-48,115), fill='#becbd5', width=2)
            draw.text((48,h-80), 'ENGINEERING PROTOTYPE — NOT A MANUFACTURING RELEASE', font=font(23), fill='#8c3c16')
            draw.text((48,h-43), f'Actual CAD tessellation | {len(shown)} components | source {validation["source_sha256"][:12]}', font=font(18), fill='#40556a')
            path = out / 'images' / f'px1_{key}.png'
            im.save(path)
            manifest['views'].append({'file':str(path.relative_to(out)), 'triangles':count,
                'shown_components':[x['id'] for x in shown],
                'hidden_components':[x['id'] for x in meshes if not include(x)],
                'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            print(path, flush=True)
    (out/'images'/'render_manifest.json').write_text(json.dumps(manifest,indent=2))


if __name__ == '__main__':
    main()
