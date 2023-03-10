import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from io import BytesIO
from mlconfig import Model
from tqdm.auto import tqdm
import torch
from point_e.models.download import load_checkpoint
from point_e.models.configs import MODEL_CONFIGS, model_from_config
from point_e.util.pc_to_mesh import marching_cubes_mesh
from point_e.util.point_cloud import PointCloud


app = FastAPI()
modelobj = Model()
sampler = modelobj.get_sampler()


class Payload(BaseModel):
    text: str


@app.post("/tt3d")
async def tt3d(payload: Payload):
    print(f'Request: {payload}')
    # Set a prompt to condition on.
    prompt = payload.text
    
    # Generate results as tensors
    samples = None
    for x in tqdm(sampler.sample_batch_progressive(batch_size=1, model_kwargs=dict(texts=[prompt]))):
        samples = x
    
    # Convert tensors to PointCloud
    pc = sampler.output_to_point_clouds(samples)[0]
    pc.save('pcimg.npz')
    
    # Create model and save as mesh.ply file
    mesh_filename = 'mesh.ply'
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('creating SDF model...')
    name = 'sdf'
    model = model_from_config(MODEL_CONFIGS[name], device)
    model.eval()
    print('loading SDF model...')
    model.load_state_dict(load_checkpoint(name, device))
    
    point_cloud_path = "pcimg.npz" #@param
    pcMesh = PointCloud.load(point_cloud_path)
    grid_size = 64 #@param {type: "integer"}
    
    # Produce a mesh (with vertex colors)
    mesh = marching_cubes_mesh(
        pc=pcMesh,
        model=model,
        batch_size=4096,
        grid_size=grid_size, # increase to 128 for resolution used in evals
        progress=True,
    )
    
    # Write the mesh to a PLY file
    with open(mesh_filename, 'wb') as f:
        mesh.write_ply(f)
    
    # Return point cloud mesh as a .ply file
    return FileResponse(mesh_filename, media_type="application/octet-stream", filename=mesh_filename)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)
