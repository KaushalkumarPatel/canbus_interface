#!/usr/bin/env python
import rospy
from canbus_interface.msg import CanFrame2
from canbus_interface.srv import CanFrameSrv
import can

class canbus_ros_interface(can.Listener):
    def __init__(self,bus):
        self.bus = bus
        # whenever a message appears on the bus, this node will try to publish it in the ros network
        notifier = can.Notifier(bus, [self])

       # self.canpub = rospy.Publisher('data', CanFrame,queue_size=10)
        self.cansrv = rospy.Service('send_frame', CanFrameSrv, self.send_message)
        self.cansub = rospy.Subscriber('data', CanFrame2, self.send_message2)

    def on_message_received(self,msg):
    #     #rospy.loginfo("received this %s"%(msg))
    #     canframe = CanFrame2()
    #     canframe.timestamp = rospy.Time.now()
    #     canframe.arbitration_id = msg.arbitration_id
    #     canframe.isExtended = msg.id_type
    #     canframe.data = [x for x in msg.data]
    #     #rospy.loginfo("sending this %s"%(canframe))
    #     self.canpub.publish(canframe)
        pass

    def send_message(self, req):
        #rospy.loginfo("sending message"%(req))
        #TODO implement this
        pass

    def send_message2(self,rcvMsg):
        if(rcvMsg.isExtended):
            isExtended=True
        else:
            isExtended=False
        msg = can.Message(arbitration_id=rcvMsg.arbitration_id, data=[x for x in rcvMsg.data], extended_id=isExtended)
        self.bus.send(msg)
        # pass

if __name__=='__main__':
    rospy.init_node('can')
    can_ifname =  rospy.get_param('~can_ifname','can0')
    rospy.loginfo("can_ifname %s"%(can_ifname))
    bus = can.interface.Bus(can_ifname)
    canros = canbus_ros_interface(bus)
    r = rospy.Rate(10)
    try:
        while not rospy.is_shutdown():
            r.sleep()
    except KeyboardInterrupt:
        bus.shutdown()

