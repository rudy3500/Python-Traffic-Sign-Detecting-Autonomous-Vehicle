import os
import sys
import time

from mathstropy.ml import load_model, model_predict
from libs.preprocessing import data_prep, feature_extraction
from mathstrovehiclesim import TrafficSignInterpretionSimulator

# load trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = script_dir + "/model/model.pkl"
#model = load_model(model_path)

d_mode = True
simulator = TrafficSignInterpretionSimulator(
  development_mode=d_mode,
  size="small",
  background_address="assets/images/simulator/default.jpg")
required_action = ""
predicted_type = ""
running = True
while running:
  vehicle_state, data = simulator.step(action=required_action,
                                    user_type=predicted_type)
  #extract perception data
  host_speed = vehicle_state['host_speed']
  host_lane = vehicle_state['host_lane']

  #predict traffic sign type
  predicted_type = data

  
  #control host vehicle base on traffic sign
  if predicted_type == "keep-right" and host_lane == 0:
    print("shifting right")
    required_action = "shift-right"
  elif predicted_type == "keep-left" and host_lane == 1:
    print("shifting left")
    required_action = "shift-left"
  elif predicted_type == "stop":
    required_action = "stop"
  elif predicted_type == "headlights-on":
    required_action = "headlights-on"
  elif predicted_type == "headlights-off":
    required_action = "headlights-off"
  elif predicted_type == "school-zone":
    if host_speed > 20: 
      required_action = "speed-down"
      host_speed = 20
      print(host_speed)
    elif host_speed < 20:
      required_action = "speed-up"
      host_speed = 20
      print(host_speed)
  elif predicted_type == "speed-limit":
    if host_speed < 40:
      required_action = "speed-up"
      host_speed = 40
      print(host_speed)
    elif host_speed > 40:
      required_action = "speed-down"
      host_speed = 40
      print(host_speed)
  else:
    required_action = ""

  
