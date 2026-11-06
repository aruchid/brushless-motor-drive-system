import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import prototype as p
class PrototypeTests(unittest.TestCase):
 def test_reference_recovery(self):
  _,_,metrics=p.demo()
  self.assertTrue(metrics)
 def test_invalid_data(self):
  with self.assertRaises(ValueError):p.finite([float('nan')])
  with self.assertRaises(ValueError):p.finite([])
 def test_reject_invalid_process_input(self):
  with self.assertRaises(ValueError):p.process([1],dt=-1)

 def test_nonfinite_controller_parameters(self):
  for name in ('dt','kp','ki','max_torque'):
   for value in (float('nan'),float('inf'),[1]):
    with self.subTest(name=name,value=value), self.assertRaises(ValueError):
     p.process([1],**{name:value})
