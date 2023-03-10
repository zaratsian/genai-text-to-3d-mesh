
import torch
from tqdm.auto import tqdm

from point_e.diffusion.configs import DIFFUSION_CONFIGS, diffusion_from_config
from point_e.diffusion.sampler import PointCloudSampler
from point_e.models.download import load_checkpoint
from point_e.models.configs import MODEL_CONFIGS, model_from_config
from point_e.util.plotting import plot_point_cloud

class Model:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        print('creating base model...')
        base_name = 'base40M-textvec'
        self.base_model = model_from_config(MODEL_CONFIGS[base_name], self.device)
        self.base_model.eval()
        self.base_diffusion = diffusion_from_config(DIFFUSION_CONFIGS[base_name])

        print('creating upsample model...')
        self.upsampler_model = model_from_config(MODEL_CONFIGS['upsample'], self.device)
        self.upsampler_model.eval()
        self.upsampler_diffusion = diffusion_from_config(DIFFUSION_CONFIGS['upsample'])

        print('downloading base checkpoint...')
        self.base_model.load_state_dict(load_checkpoint(base_name, self.device))

        print('downloading upsampler checkpoint...')
        self.upsampler_model.load_state_dict(load_checkpoint('upsample', self.device))

    def get_sampler(self):
        sampler = PointCloudSampler(
            device=self.device,
            models=[self.base_model, self.upsampler_model],
            diffusions=[self.base_diffusion, self.upsampler_diffusion],
            num_points=[1024, 4096 - 1024],
            aux_channels=['R', 'G', 'B'],
            guidance_scale=[3.0, 0.0],
            model_kwargs_key_filter=('texts', ''),
        )
        return sampler
