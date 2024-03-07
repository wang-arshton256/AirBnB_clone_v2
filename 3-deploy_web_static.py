#!/usr/bin/python3
"""Script that deploys static web pages to remote servers"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.25.111.63', '52.205.93.131']

def do_pack():
    """Method that creates a .tgz archive in the local directory of a codebase
    using operations found in the fabric python module (local)"""
    
    if not os.path.exists('versions'):
        os.makedirs('versions')
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(now)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None
        

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
            
def deploy():
    """Deploys Static web pages to web server
    """
    
    new_archive_path = do_pack()
    if new_archive_path is None:
        return False
    else:
        result = do_deploy(new_archive_path)
        return result
