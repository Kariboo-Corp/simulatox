import back_end.commands.control as c
def move(x,y,z,node:c.OffboardControl):
    print("Moving node from",node.local_pos() ," to ",x,y,z)
    node.moveto(x,y,z)
    c.executor_restart()
def get_position(node:c.OffboardControl):
    return node.local_pos()
