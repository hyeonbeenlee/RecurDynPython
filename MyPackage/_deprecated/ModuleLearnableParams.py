import torch

class LearnableParams(torch.nn.Module):
	def RegisterAlpha(self,init_value:float=0):
		self.alpha = torch.tensor([init_value], dtype=torch.float32, requires_grad=True, device='cuda')
		self.alpha=torch.nn.Parameter(self.alpha)
		self.register_parameter('alpha', self.alpha)
	
	def RegisterBeta(self,init_value:float=0):
		self.beta = torch.tensor([init_value], dtype=torch.float32, requires_grad=True, device='cuda')
		self.beta=torch.nn.Parameter(self.beta)
		self.register_parameter('beta', self.beta)
		
	def RegisterGamma(self,init_value:float=0):
		self.gamma = torch.tensor([init_value], dtype=torch.float32, requires_grad=True, device='cuda')
		self.gamma=torch.nn.Parameter(self.gamma)
		self.register_parameter('gamma', self.gamma)