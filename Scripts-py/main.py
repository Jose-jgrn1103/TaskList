"""Script de inicialização do projeto"""

import sys
from interface import TaskListInterface
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    # Cria uma aplicação Qt
    application = QApplication(sys.argv)

    # Define uma instância de TaskListInterface e a exibe
    interface = TaskListInterface()
    interface.show()

    # Inicializa o loop de execução da aplicação
    sys.exit(application.exec_())
