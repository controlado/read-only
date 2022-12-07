"""Deixa as configurações do lol em modo somente leitura.

Discord: Balaclava#1912
GitHub: https://github.com/controlado
"""

import os
from contextlib import suppress
from json import dump, load
from stat import S_IREAD, S_IWUSR
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askretrycancel, askyesno


class ReadOnly:
    """Deixa as configurações do lol em modo somente leitura.

    A finalidade é automatizar o processo de muitas pessoas que
    tem diversas contas e ficam alterando elas com frequência.
    """

    __app_data = os.getenv("APPDATA")
    __app_settings_filename = "settings.json"
    __app_settings_path = f"{__app_data}/ro-league"
    __app_settings_file_path = f"{__app_settings_path}/{__app_settings_filename}"

    def __init__(self) -> None:
        """Faz os preparativos pra o aplicativo.

        Tenta puxar as configurações do aplicativo e caso não
        exista: cria a pasta padrão de configurações do app.
        """
        self.league_config_path: str
        self.app_settings = self.__get_app_settings()

        if not self.app_settings:  # se não existir uma configuração.
            self.create_folder(self.__app_settings_path)
        else:
            self.league_config_path = self.app_settings["lolPath"]

    @staticmethod
    def create_folder(path: str) -> None:
        """Cria uma pasta evitando erros."""
        with suppress(FileExistsError):
            os.mkdir(path)

    @staticmethod
    def get_files(path: str) -> list | None:
        """Puxa os arquivos de um diretório evitando erros."""
        with suppress(FileNotFoundError):
            return os.listdir(path)

    @staticmethod
    def get_local_disk() -> str:
        """Puxa o disco local onde está o ProgramFiles."""
        program_files = os.environ["ProgramFiles"]
        return program_files.split("Program")[0]

    def app(self) -> None:
        """Inicia o aplicativo.

        Verifica se já existe uma configuração do usuário e caso contrário
        ele vai pedir a mesma chamando a função get_league_path().

        Com a configuração do usuário pronta, o app salva ela localmente pra
        usos futuros do aplicativo, pra evitar pedir a configuração de novo.

        Por fim, o app pergunta se quer ativar ou desativar as permissões e
        aplica as mudanças dependendo da escolha do usuário.
        """
        if not self.app_settings:
            self.league_config_path = self.__get_league_path()
            self.__create_app_settings()

        enable = askyesno("Balaclava#1912", "Deseja habilitar as permissões?")
        self.__change_permission(enable)

    def __get_league_path(self) -> str:
        """Pede a localização do lol ao usuário."""
        initial_dir = self.get_local_disk()
        file_types = [("LoL", "LeagueClient.exe")]

        while True:
            league_file = askopenfilename(
                title="Escolha o LeagueClient",
                initialdir=initial_dir,
                filetypes=file_types
            )
            league_path = os.path.dirname(league_file)
            league_config_path = f"{league_path}/Config"

            if self.get_files(league_config_path):
                break

            if not askretrycancel("Balaclava#1912", "Diretório errado."):
                exit("O usuário escolheu cancelar o processo.")

        return league_config_path

    def __get_app_settings(self) -> dict | None:
        """Tenta puxar a configuração local do aplicativo."""
        with suppress(FileNotFoundError):
            with open(self.__app_settings_file_path, "r", encoding="UTF-8") as opened_file:
                return load(opened_file)

    def __create_app_settings(self) -> None:
        """Cria e salva localmente as configurações do aplicativo."""
        self.app_settings = {"lolPath": self.league_config_path}
        with open(self.__app_settings_file_path, "w", encoding="UTF-8") as opened_file:
            dump(self.app_settings, opened_file, indent=4, ensure_ascii=False)

    def __change_permission(self, enable: bool) -> None:
        """Muda as permissões de escrita dos arquivos de configuração do lol."""
        league_config_files = ("game.cfg", "input.ini", "PersistedSettings.json")
        permission = S_IWUSR if enable else S_IREAD

        for filename in league_config_files:
            file_path = f"{self.league_config_path}/{filename}"
            os.chmod(file_path, permission)


def main():
    """Inicia o aplicativo corretamente."""
    rol = ReadOnly()
    rol.app()


if __name__ == "__main__":
    main()
