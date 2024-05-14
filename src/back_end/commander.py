import back_end.commands.control as c

def move(x,y,z,node:c.OffboardControl):
    print("Moving node from",node.local_pos() ," to ",x,y,z)
    node.moveto(x,y,z)
    if(node.vehicle_status.nav_state != c.VehicleStatus.NAVIGATION_STATE_OFFBOARD):
        node.engage_offboard_mode()
    c.executor_restart()
def arm_all_drones(nodes):
    for node in nodes:
        node.engage_offboard_mode()
        node.arm()
    c.executor_restart()
def get_position(node:c.OffboardControl):
    return node.local_pos()
