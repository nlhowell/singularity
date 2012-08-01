# Copyright (C) 2012 by Alex Brandt <alunduil@alunduil.com>
#
# singularity is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from singularity.communicators import Communicator

logger = logging.getLogger(__name__) # pylint: disable=C0103

class XenCommunicator(Communicator):
    """An attempt at introspecting the Openstack communication protocol.

    ### Description

    Reads from xenbus using the xen module and responding via the same
    mechanism.

    ### Notes

    Found the key!  /local/domain/<dom_id>
    To get the key: dom_id

    Although, once one knows this secret they can open up the following data
    structue with a xenstore ls /local/domain/<dom_id>:

    vm = "/vm/9a180993-ef93-6d0a-66bd-32557faa106e"
    vss = "/vss/9a180993-ef93-6d0a-66bd-32557faa106e"
    name = "slice21006919"
    cpu = ""
     0 = ""
      availability = "online"
     1 = ""
      availability = "online"
     2 = ""
      availability = "online"
     3 = ""
      availability = "online"
    memory = ""
     initial-reservation = "533504"
     static-max = "524288"
     target = "524288"
     dynamic-min = "524288"
     dynamic-max = "524288"
     memory-offset = "0"
    device = ""
     vbd = ""
      51744 = ""
       backend = "/local/domain/0/backend/vbd/89/51744"
       protocol = "x86_64-abi"
       state = "4"
       backend-id = "0"
       device-type = "disk"
       virtual-device = "51744"
       ring-ref = "8"
       event-channel = "27"
      51712 = ""
       backend = "/local/domain/0/backend/vbd/89/51712"
       protocol = "x86_64-abi"
       state = "4"
       backend-id = "0"
       device-type = "disk"
       virtual-device = "51712"
       ring-ref = "9"
       event-channel = "28"
     vif = ""
      0 = ""
       backend = "/local/domain/0/backend/vif/89/0"
       backend-id = "0"
       state = "4"
       handle = "0"
       mac = "40:40:97:83:78:2e"
       disconnect = "0"
       protocol = "x86_64-abi"
       tx-ring-ref = "10"
       rx-ring-ref = "1280"
       event-channel = "29"
       request-rx-copy = "1"
       feature-rx-notify = "1"
       feature-sg = "1"
       feature-gso-tcpv4 = "1"
      1 = ""
       backend = "/local/domain/0/backend/vif/89/1"
       backend-id = "0"
       state = "4"
       handle = "1"
       mac = "40:40:a1:47:e2:af"
       disconnect = "0"
       protocol = "x86_64-abi"
       tx-ring-ref = "1281"
       rx-ring-ref = "1282"
       event-channel = "30"
       request-rx-copy = "1"
       feature-rx-notify = "1"
       feature-sg = "1"
       feature-gso-tcpv4 = "1"
    error = ""
    drivers = ""
    control = ""
     platform-feature-multiprocessor-suspend = "1"
     feature-balloon = "1"
    attr = ""
     eth0 = ""
      ip = "xxx.xxx.xxx.xxx"
     eth1 = ""
      ip = "xxx.xxx.xxx.xxx"
     PVAddons = ""
      MajorVersion = "5"
      MinorVersion = "6"
      MicroVersion = "100"
      BuildVersion = "39153"
      Installed = "1"
    data = ""
     host = ""
     meminfo_total = "504076"
     meminfo_free = "159156"
     os_name = "gentoo"
     os_majorver = "2"
     os_minorver = "1"
     os_uname = "3.4.2-hardened-r1"
     os_distro = "gentoo"
     updated = "Tue Jul 31 20:09:21 CDT 2012"
    messages = ""
    vm-data = ""
     networking = ""
      40409783782e = "{"label":"public","ips":[{"netmask":"255.255.255.0","\..."
      4040a147e2af = "{"label":"private","ips":[{"netmask":"255.255.128.0",\..."
    platform = ""
     apic = "true"
     viridian = "true"
     acpi = "true"
     pae = "true"
     nx = "false"
     vcpu = ""
      number = "4"
      weight = "12"
    bios-strings = ""
     bios-vendor = "Xen"
     bios-version = ""
     system-manufacturer = "Xen"
     system-product-name = "HVM domU"
     system-version = ""
     system-serial-number = ""
     hp-rombios = ""
     oem-1 = "Xen"
     oem-2 = "MS_VM_CERT/SHA1/bdbeb6e0a816d43fa6d3fe8aaef04c2bad9d3e3d"
    unique-domain-id = "d5c91743-ae4b-cfe6-1976-04dde8c18fce"
    domid = "89"
    store = ""
     port = "1"
     ring-ref = "4912920"
    serial = ""
     0 = ""
      limit = "65536"
      tty = "/dev/pts/6"
      vncterm-pid = "18571"
      vnc-port = "5906"
    console = ""
     port = "2"
     ring-ref = "4912919"
     tty = "/dev/pts/6"

    Everything at the top level is directly accessible with xenstore (e.g.
    xenstore ls serial).  

    ### Communication

    The point of this method is to get information from the hypervisor, process
    that information, and then respond correctly.

    A special file (preferably universally unique) is used as the communication
    mechanism to talk with the host.  An example of one of these requests is
    shown here (JSON is the communication protocol):

    If the hypervisor runs the command version:
    >>> xenstore write data/host/d1e9770a-b30d-2320-6407-b27a2f7ed177 '{"name":"version", "value":"agent"}'

    The agent should respond with the following:
    >>> xenstore read data/guest/d1e9770a-b30d-2320-6407-b27a2f7ed177
    '{"message": "0.0.1.37", "returncode": "0"}'

    The commands the hypervisor may send (grabbed from openstack agent source:
    common/agent-client.py):

    * password
    * version
    * features
    * agentupdate
    * resetnetwork
    * injectfile
    * kmsactivate
    * help # Registered as a command but only acts locally.

    Hostname is available in vm-data/hostname.
    IP information is available in vm-data/networking.

    """

    def send(self):
        pass

    def receive(self):
        pass
