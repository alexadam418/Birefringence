test = {'state': {'error': '', 'flags': {'cancelling': False, 'closedOrError': False, 'error': False,
                                         'finishing': False, 'operational': True, 'paused': False,
                                         'pausing': False, 'printing': False, 'ready': True, 'resuming': False,
                                         'sdReady': False}, 'text': 'Operational'}}
test2 = test.get('state', {}).get('flags', {}).get('sdReady')
if test2:
    print(1)
else:
    print(2)
print(test2)
