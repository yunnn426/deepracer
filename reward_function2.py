import math

ABS_STEERING_THRESHOLD = 15 

def reward_function(params):
   # declare parameters
   on_track = params['all_wheels_on_track']
   closest_waypoints = params['closest_waypoints']
   waypoints = params['waypoints']
   track_width = params['track_width']
   steering_angle = params['steering_angle']
   speed = params['speed']
   heading = params['heading']
   distance_from_center = params['distance_from_center']

   reward = 1 # default reward

   if on_track:
       # 1) speed
       if is_steering(steering_angle): # corner
           if speed < 1.5:
               reward += 2
           else:
               reward -= 1
       else:
           if speed > 3:
               reward += 7
           else:
               reward *= 0.6

       # 2) angle diff from waypoints
       next_point = waypoints[closest_waypoints[1]]
       prev_point = waypoints[closest_waypoints[0]]
       direction_diff = calc_direction_diff(next_point, prev_point, heading)
      
       if direction_diff < 10:
           reward += 5
       else:
           reward *= 0.5

       # 3) stay at center line
       marker_1 = 0.1 * track_width
       marker_2 = 0.3 * track_width
       marker_3 = 0.5 * track_width
       if distance_from_center <= marker_1:
           reward += 5
       elif distance_from_center <= marker_2:
           reward += 2
       elif distance_from_center <= marker_3:
           reward += 1
       else:
           reward *= 0.5

       # 4) steering
       if steering_angle < 15:
           reward += 8
       else:
           reward -= 1

       # tune waypoints
       # 5) waypoint 28~40 turn left
       if (closest_waypoints[0] or closest_waypoints[1]) in [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]:
           if steering_angle > 5: # if steering to left
               reward += 5
           else:
               reward -= 5
      
       # 6) waypoint 0~15, 90~104 speed up
       if (closest_waypoints[0] or closest_waypoints[1]) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                                                             90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]:
           if speed > 3.5:
               reward += 15
           else:
               reward *= 0.5
   else:
       reward *= 0.2
      
   return float(reward)

def is_steering(steering_angle):
   if abs(steering_angle) > ABS_STEERING_THRESHOLD:
       return True

def calc_direction_diff(next_point, prev_point, heading):
   track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
   track_direction = math.degrees(track_direction)
   direction_diff = abs(track_direction - heading)
   if direction_diff > 180:
       direction_diff = 360 - 180
   return direction_diff

