from os.path import abspath, basename

from testcontainers.core.container import DockerContainer


class BeetsContainer(DockerContainer):
    def __init__(self, tag='1.6.0', music_dir=None, config_dir=None, package_src_dirs=[], packages=[]):
        super(BeetsContainer, self).__init__(f'linuxserver/beets:{tag}')

        self.package_src_dirs = [(hash(abspath(p)), abspath(p)) for p in package_src_dirs]
        self.packages = packages

        for name, path in self.package_src_dirs:
            self.with_volume_mapping(path, f'/src-tmp/{name}')

        if config_dir:
            self.with_volume_mapping(abspath(config_dir), '/config-tmp')

        if music_dir:
            self.with_volume_mapping(abspath(music_dir), '/music-tmp')

    def start(self):
        super(BeetsContainer, self).start()

        self.install_packages()

        self.exec('mkdir /music')
        self.exec('cp -r /music-tmp /music')
        self.exec('cp /config-tmp/config.yaml /config')

        self.command('import /music')

    def command(self, command):
        _command = f'beet {command}'
        print(_command)

        result = self.exec(_command).output.decode('utf-8')
        print(result)

        return [r for r in result.splitlines() if r]

    def list(self, query=''):
        return self.command(f'list {query}')

    def install_packages(self):
        for name, path in self.package_src_dirs:
            module_name = basename(path)

            print(f'Installing package from source {path}')
            self.exec(f'cp -a /src-tmp/{name}/. {self._get_site_packages_dir()}/{module_name}/')

        for package in self.packages:
            print(f'Installing package {package}')
            self.exec(f'pip3 install {package}')

    def _get_site_packages_dir(self):
        cmd = 'python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"'
        return self.exec(cmd).output.decode('utf-8').strip()
