import torch
import torch.nn as nn

class PnP(nn.Module):
    '''
    Plug-and-Play (PnP) / Regularization bu Denoising (RED) algorithms for Image Restoration. Consists in replacing prox_g or grad_g with a denoiser.
    '''
    def __init__(self, denoiser, init=None, stepsize=1., sigma_denoiser=0.05, max_iter=50, device = torch.device('cpu')):
        super().__init__()

        self.denoiser = denoiser
        self.max_iter=max_iter
        self.device=device
        self.init = init
        self.denoiser = denoiser
            
        if isinstance(sigma_denoiser, float):
            sigma_denoiser = [sigma_denoiser] * self.max_iter
        elif isinstance(sigma_denoiser, list):
            assert len(sigma_denoiser) == self.max_iter
        else:
            raise ValueError('sigma_denoiser must be either int/float or a list of length max_iter') 

        if isinstance(stepsize, float):
            stepsize = [stepsize] * self.max_iter
        elif isinstance(stepsize, list):
            assert len(stepsize) == self.max_iter
        else:
            raise ValueError('stepsize must be either int/float or a list of length max_iter') 

        # if self.unroll :
        #     self.register_parameter(name='sigma_denoiser',
        #                     param=torch.nn.Parameter(torch.tensor(sigma_denoiser, device=self.device),
        #                     requires_grad=True))
        #     self.register_parameter(name='stepsize',
        #                     param=torch.nn.Parameter(torch.tensor(stepsize, device=self.device),
        #                     requires_grad=True))
        # else:
        self.stepsize = stepsize
        self.sigma_denoiser = sigma_denoiser
    
    # def prox_g(self,x,it):
    #     return self.denoiser(x, self.sigma_denoiser[it])
    def prox_g(self, x, sigma):
        return self.denoiser(x, sigma)

    def grad_g(self,x,it):
        return x-self.denoiser(x, self.sigma_denoiser[it])

    def update_stepsize(self,it):
        return self.stepsize[it]