profile = 'docker'
if profile == 'aws':
    from .control_aws_login import *
elif profile == 'docker':
    from .control_dock_login import *
elif profile == 'hadoop':
    from .control_hadoop_login import *
else:
    pass
