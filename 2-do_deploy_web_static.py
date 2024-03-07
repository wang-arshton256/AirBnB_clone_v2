#!/usr/bin/python3
"""Script that deploys and distributes archive
to the remote server"""

from fabric.api import *
import os

env.hosts = ['100.25.111.63', '52.205.93.131']

def do_deploy(archive_path):
    """Deploy archive to the web servers"""
    
    if not os.path.exists(archive_path):
        return False
    else:
        try:
            filename = archive_path.split('/')[-1]
            directory_name = filename.split('.')[0]
            directory_path = "/data/web_static/releases/{}".format(directory_name)
            
            put(archive_path, '/tmp/{}'.format(filename))
            run('mkdir -p {}'.format(directory_path))
            run('tar -xzf /tmp/{} -C {}'.format(filename, directory_path))
            run('rm /tmp/{}'.format(filename))
            run('mv {}/web_static/* {}'.format(directory_path, directory_path))
            run('rm -rf {}/web_static'.format(directory_path))
            run('rm -rf /data/web_static/current')
            run('ln -s {} /data/web_static/current'.format(directory_path))
            return True
        except:
            return False
