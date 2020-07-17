"""
fabric部署过程
1、远程连接服务器。
2、进入项目根目录，从仓库拉取最新的代码。
3、如果项目引入了新的依赖，需要执行 pip install -r requirements.txt 安装最新的依赖。
4、如果修改或新增了项目静态文件，需要执行 python manage.py collectstatic 收集静态文件。
5、如果数据库发生了变化，需要执行 python manage.py migrate 迁移数据库。
6、重启Nginx和Gunicorn是改动生效。
"""
from fabric import task
from invoke import Responder
from _credentials import github_password, github_username


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'http://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'http://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return  [username_responder, password_responder]

@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'hellodjango-blog-tutorial'

    project_root_path = '~/apps/HelloDjango-blog-tutorial/'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖， 迁移数据库， 收集静态文件
    with c.cd(project_root_path):
        c.run('source activate Django')
        c.run('pip install -r requirements.txt')
        c.run('python manage.py migrate')
        c.run('python collectstatic --noinput')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)