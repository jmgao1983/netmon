device_netcap = {
    'cisco': {
        'prompt': '#',
        'page': 'terminal len 0',
        'conf': ['sh run'],
        'routesum': ['sh ip route sum'],
        'route': ['sh ip route'],
        'mod': ['sh module', 'sh invent', 'sh envi status'],
        'int': ['sh int status', 'sh ip int b'],
        'stp': ['sh spanning-tree root id'],
    },
    'h3c': {
        'prompt': '>',
        'page': 'screen-length disable',
        'conf': ['disp curr'],
        'routesum': ['disp ip rout stat'],
        'route': ['disp ip rout'],
        'mod': ['disp device', 'disp power', 'disp fan'],
        'int': ['disp int brief'],
        'stp': ['disp stp root', 'disp stp brief'],
    },
    'huawei': {
        'prompt': '>',
        'page': 'screen-length 0 temporary',
        'conf': ['disp curr'],
        'routesum': ['disp ip rout stat'],
        'route': ['disp ip rout'],
        'mod': ['disp device', 'disp power', 'disp fan'],
        'int': ['disp int brief'],
        'stp': ['disp stp bri root', 'disp stp brief'],
    },
    'junos': {
        'prompt': '>',
        'page': 'set cli screen-length 0',
        'conf': ['show configuration | display set'],
        'routesum': ['show route summary'],
        'route': ['show route terse'],
        'mod': [
            'show chassis hardware detail',
            'show chassis environment'
        ],
        'int': ['show interfaces terse'],
        'stp': [
            'show spanning-tree interface',
            'show spanning-tree bridge | match root'
        ],
    },
    'dell': {
        'prompt': '#',
        'page': 'terminal len 0',
        'conf': ['sh run'],
        'routesum': ['sh ip route sum'],
        'route': ['sh ip route'],
        'mod': ['sh module', 'sh invent', 'sh envi'],
        'int': ['sh int status', 'sh ip int b'],
        'stp': ['sh spanning-tree root id'],
    },
}

device_netmon = {
    'cisco': {
        'succ': 'min/avg/max = [0-9]([0-9])*',
        'fail': 'Success rate is 0 percent',
        'ping': 'ping\n\n%s\n2\n\n\n\n\n',
    },
    'h3c': {
        'succ': 'min/avg/max(\/std-dev)* = [0-9]([0-9])*',
        'fail': '100.00*% packet loss',
        'ping': 'ping -c 2 %s',
    },
    'huawei': {
        'succ': 'min/avg/max(\/std-dev)* = [0-9]([0-9])*',
        'fail': '100.00*% packet loss',
        'ping': 'ping -c 2 %s',
    },
    'junos': {
        'succ': 'min/avg/max/stddev = [0-9]([0-9])*',
        'fail': '100% packet loss',
        'ping': 'ping count 2 %s',
    },
    'linux': {
        'succ': 'min/avg/max/mdev = [0-9]([0-9])*', 
        'fail': '100% packet loss',
        'ping':  'ping -c 2 %s',
    },
}
