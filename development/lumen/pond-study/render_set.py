"""Publish complete, immutable sets of views from one saved Blender scene."""
from array import array
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

import bpy

COMMON = ('Ground', 'Water', 'Planting', 'Boundary', 'Fittings')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def geometry_hash(groups):
    """Hash evaluated shared meshes, including paving and their transforms."""
    digest=hashlib.sha256();deps=bpy.context.evaluated_depsgraph_get()
    for group in COMMON:
        for ob in sorted(groups[group].objects,key=lambda o:o.name):
            if ob.type!='MESH':continue
            digest.update((group+'\0'+ob.name+'\0').encode())
            evaluated=ob.evaluated_get(deps);mesh=evaluated.to_mesh()
            try:
                xyz=array('f',[0])*(len(mesh.vertices)*3)
                mesh.vertices.foreach_get('co',xyz)
                digest.update(xyz.tobytes())
                indices=array('i',[0])*len(mesh.loops)
                mesh.loops.foreach_get('vertex_index',indices)
                digest.update(indices.tobytes())
                digest.update(repr([list(row) for row in evaluated.matrix_world]).encode())
            finally:evaluated.to_mesh_clear()
    return digest.hexdigest()


def stage():
    return Path(tempfile.mkdtemp(prefix='lumen-pond-render-'))


def publish(here,work,views,common_hash,inputs):
    """Expose no new set until all required renders and the saved file exist."""
    snapshot=work/'pond-study.blend'
    for name in views:
        if not (work/'renders'/f'{name}.png').is_file():raise RuntimeError('Missing view: '+name)
    blend_hash=sha(snapshot)
    build_id=blend_hash[:16]
    relative=Path('builds')/build_id
    manifest={
        'schema_version':1,'build_id':build_id,
        'built_utc':datetime.now(timezone.utc).isoformat(),
        'blend':{'path':str(relative/'pond-study.blend'),'sha256':blend_hash},
        'common_geometry_sha256':common_hash,
        'views':{name:{'path':str(relative/'renders'/f'{name}.png'),
                       'sha256':sha(work/'renders'/f'{name}.png'),
                       'common_geometry_sha256':common_hash,
                       'snapshot_sha256':blend_hash} for name in views},
        'inputs':inputs,
        'state_note':'Pond, overview and action views share unchanged ground, water, planting and boundary meshes. The wheel and figure collections are separate depicted states. Section is derived from the same bed and paving.',
    }
    (work/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (here/'builds').mkdir(exist_ok=True)
    destination=here/relative
    if destination.exists():raise RuntimeError('Render bundle already exists: '+str(destination))
    shutil.move(str(work),str(destination))
    # The review always uses immutable build URLs. Compatibility links make
    # direct .blend and renders/ paths point to the same completed bundle too.
    backup=None
    for name,target in [('pond-study.blend',relative/'pond-study.blend'),('renders',relative/'renders')]:
        alias=here/name
        if alias.exists() and not alias.is_symlink():
            if backup is None:backup=Path(tempfile.mkdtemp(prefix='lumen-pond-previous-'))
            shutil.move(str(alias),str(backup/name))
        link=here/(name+'.next')
        if link.is_symlink():link.unlink()
        link.symlink_to(target,target_is_directory=name=='renders')
        link.replace(alias)
    raw=json.dumps(manifest,indent=2)+'\n'
    (here/'render-manifest.json.next').write_text(raw)
    (here/'render-manifest.json.next').replace(here/'render-manifest.json')
    (here/'render-manifest.js.next').write_text('window.POND_RENDER_SET = '+raw.strip()+';\n')
    (here/'render-manifest.js.next').replace(here/'render-manifest.js')
    return manifest
