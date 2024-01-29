#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import math
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

class MoveGroupPythonInterfaceTutorial(object):
    def __init__(self, group_name):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

        self.group = moveit_commander.MoveGroupCommander(group_name)

    def get_current_joint_values(self):

        return self.group.get_current_joint_values()

    def set_joint_goal(self, target_joints):
 
        self.group.set_joint_value_target(target_joints)

    def go_to_joint_state(self):

        plan = self.group.plan()
        self.group.go(wait=True)

    def close(self):

        moveit_commander.roscpp_shutdown()

    def Pos(self, mode, val=0, left=True, down=True):
        current_joints=self.group.get_current_joint_values()
        if mode == "reset":
            self.Pos("open")
            time.sleep(1)
            target_joints=[0, 0.1745, 0, 0, 0.1745, 0, 0, 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state()            
            return None
        elif mode == "open":
            target_joints=[0, 0.1745, current_joints[2], 0, 0.1745, current_joints[5], 0, 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state()
        elif mode == "close":  
            target_joints=[3*val, 0.1745, current_joints[2], 3*val, 0.1745, current_joints[5], 3*val, 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state() 
        elif mode == "adduct":  
            target_joints=[current_joints[0], 0.1745, -1.57, current_joints[3], 0.1745, 1.57, current_joints[6], 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state()
        elif mode == "pinch_close":
            if current_joints[2] < -0.75:
                self.Pos("reset")
                time.sleep(1.5)
                current_joints=self.group.get_current_joint_values()  
            target_joints=[current_joints[0], 0.1745, 0, 3*val, 0.1745, 0, 3*val, 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state()  
        elif mode == "power_close":
            if current_joints[2] > -0.75:
                self.Pos("open")
                time.sleep(1)
                current_joints=self.group.get_current_joint_values()
                self.Pos("adduct")
                time.sleep(1)
                current_joints=self.group.get_current_joint_values()   
            target_joints=[3*val, 0.1745, current_joints[2], 3*val, 0.1745, current_joints[5], 3*val, 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state()
        elif mode =="pinch_object_move":
            if current_joints[2] < -0.75:
                print( '[ERR] Hand is not in a pinch grasp')
                return None
            else:
                if left==True and down==True:
                    target_joints=[current_joints[0], 0.1745, 0, current_joints[3]-val, 0.1745, 0, current_joints[6]-val, 0.1745]
                    self.set_joint_goal(target_joints) 
                    self.go_to_joint_state()
                elif left==True and down==False:
                    target_joints=[current_joints[0], 0.1745, 0, current_joints[3]+val, 0.1745, 0, current_joints[6]-val, 0.1745]
                    self.set_joint_goal(target_joints) 
                    self.go_to_joint_state()
                elif left==False and down==True:
                    target_joints=[current_joints[0], 0.1745, 0, current_joints[3]+val, 0.1745, 0, current_joints[6]+val, 0.1745]
                    self.set_joint_goal(target_joints) 
                    self.go_to_joint_state()
                else: 
                    target_joints=[current_joints[0], 0.1745, 0, current_joints[3]-val, 0.1745, 0, current_joints[6]+val, 0.1745]
                    self.set_joint_goal(target_joints) 
                    self.go_to_joint_state()
        elif mode =="hold":
            target_joints=[current_joints[0], 0.1745, current_joints[2], current_joints[3]+0.025, 0.1745, current_joints[5], current_joints[6]+0.025, 0.1745]
            self.set_joint_goal(target_joints) 
            self.go_to_joint_state()
        

        else: 
            print("Invalid mode") 
            return None

# main program
def main():
    try:
        tutorial = MoveGroupPythonInterfaceTutorial("hand")

        current_joints = tutorial.get_current_joint_values()
        rospy.loginfo("Current joint values: " + str(current_joints))

        tutorial.Pos("close",val=0.5)

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return
    finally:
        tutorial.close()

if __name__ == '__main__':
    main()