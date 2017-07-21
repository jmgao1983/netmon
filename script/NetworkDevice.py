device = {
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
        'page': 'screen-length 0',
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
