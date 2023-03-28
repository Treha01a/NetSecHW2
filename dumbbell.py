# CMU 18731 HW2
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash

#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os

# Parse arguments

parser = ArgumentParser(description="Shrew tests")
parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links",
                    required=True)
parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    required=True)
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default='10ms')
parser.add_argument('--n',
                    dest="n",
                    type=int,
                    action="store",
                    help="Number of nodes in one side of the dumbbell.",
                    required=True)

parser.add_argument('--maxq',
                    dest="maxq",
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=1000)

# Expt parameters
args = parser.parse_args()

class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self, n=6, bw_net=10, delay='20ms', bw_host=10, maxq=None):
    #TODO: Add your code to create topology
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        
        hostl1 = self.addHost('hl1')
        hostl2 = self.addHost('hl2')
        hostr1 = self.addHost('hr1')
        hostr2 = self.addHost('hr2')
        attacker1 = self.addHost('a1')
        attacker2 = self.addHost('a2')

        self.addLink(hostl1, switch1, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(hostl2, switch1, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(attacker1, switch1, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(hostr1, switch2, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(hostr2, switch2, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(attacker2, switch2, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(switch1, switch2, bw=bw_net, delay=delay, max_queue_size=maxq)		

def bbnet():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(n=args.n, bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    dumpNodeConnections(net.hosts)

    #TODO: Add your code to test reachability of hosts
    net.pingAll()

    #TODO: Add yoour code to start long lived TCP flows 
    hl1, hl2, hr1, hr2 = net.get('hl1', 'hl2', 'hr1', 'hr2')
    hl1.cmd("iperf -s -p 5001 &")
    hl2.cmd("iperf -s -p 5002 &")
    hr1.cmd("iperf -c %s -t 180 -p 5001 &"%hl1.IP())
    hr2.cmd("iperf -c %s -t 180 -p 5002 &"%hl2.IP())
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    bbnet()
