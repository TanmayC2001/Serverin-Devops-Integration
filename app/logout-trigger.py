profile = 'docker'
if profile == 'aws':
    from . import control_aws_logout
elif profile == 'docker':
    from . import control_dock_logout
elif profile == 'hadoop':
    from . import control_hadoop_logout
else:
    pass
