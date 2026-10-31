"""电机闭环控制仿真 — deterministic numerical prototype."""
import argparse,json
from pathlib import Path
import numpy as np

def finite(a,ndim=None):
 a=np.asarray(a,dtype=float)
 if not np.isfinite(a).all() or not a.size or (ndim is not None and a.ndim!=ndim): raise ValueError('Invalid shape, empty or nonfinite input')
 return a
def process(target,dt=.005,kp=.035,ki=.08,max_torque=.3):
 target=finite(target,1)
 if dt<=0 or kp<0 or ki<0 or max_torque<=0: raise ValueError('Invalid controller parameters')
 speed=0.;integral=0.;speeds=[];torques=[]
 for reference in target:
  error=reference-speed;trial=integral+error*dt;requested=kp*error+ki*trial
  torque=float(np.clip(requested,-max_torque,max_torque))
  if abs(requested)<=max_torque or error*requested<0:integral=trial
  speed+=dt*(torque-.001*speed)/.002
  speeds.append(speed);torques.append(torque)
 return np.array(speeds),np.array(torques)

def demo():
 x=np.arange(1200)*.005;target=np.where(x<1,0.,100.);speed,torque=process(target)
 assert abs(speed[-1]-100)<.5 and np.max(np.abs(torque))<=.3
 return x,{'Reference rad/s':target,'Simulated rad/s':speed},{'steady_error_rad_s':float(abs(speed[-1]-100)),'peak_torque_Nm':float(np.max(np.abs(torque)))}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('artifacts'));args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 x,series,metrics=demo()
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 if x is None:
  fig,axes=plt.subplots(1,len(series),figsize=(14,4),layout='constrained');axes=np.atleast_1d(axes)
  for ax,(label,values) in zip(axes,series.items()):ax.imshow(values,cmap='viridis');ax.set_title(label);ax.set_axis_off()
 else:
  fig,ax=plt.subplots(figsize=(11,5),layout='constrained')
  for label,values in series.items():ax.plot(x,values,label=label)
  ax.legend();ax.grid(alpha=.2)
 fig.suptitle('Synthetic prototype validation — not field measurements')
 fig.savefig(args.output/'result.png',dpi=140);plt.close(fig)
 np.savez_compressed(args.output/'results.npz',**{str(i):v for i,v in enumerate(series.values())})
 (args.output/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
