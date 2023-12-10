"""Script de funcionalidades complementares"""

import unicodedata, qtawesome
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QListWidgetItem, QWidget, QGridLayout, QLabel, QCheckBox, QPushButton, QSpacerItem,
                             QSizePolicy)


class TaskItem(QListWidgetItem):
    """Item que respresenta a tarefa"""

    # Atributo do visual do item
    _VISUAL = """
            /*Estilo rótulo da menssagem*/
            #task{
                font: 23px Arial;
            }
    """

    def __init__(self, menssage_task: str, data_base: 'TaskDataBasse'):
        """
        Configura a istância de TaskItem

        Args:
            menssage_task (str): Messagem da tarefa
            data_base (TaskDataBasse): banco de dados do projeto
        """

        # Chama o construtor da classe pai para inicializar a instância
        super().__init__()

        self._db = data_base

        # Cria um widget para o item e uma grid
        self.widget, grid = QWidget(), QGridLayout()

        # Estabele o estilo do item
        self.widget.setStyleSheet(self._VISUAL)

        # Cria o rótulo da tarefa
        self._task = QLabel(menssage_task)
        self._task.setObjectName('task')

        # Define uma caixa de check que define se a tarefa já foi realizada
        self.checkBoxItem = QCheckBox()
        self.checkBoxItem.setToolTip('Conclude Task')
        self.checkBoxItem.clicked.connect(lambda: self._db.changeStateChecked(self.data(Qt.UserRole)))  # Altera, no banco de dados, o estado da checkBoxItem
        self.checkBoxItem.stateChanged.connect(self._concludeTask)  # Chama _concludeTask() para atualizar o visual da mensagem da tarefa.

        # Gera um botão que execlui a task
        button_deleteTask = QPushButton()
        button_deleteTask.setIcon(qtawesome.icon('mdi.delete', scale_factor=1.5))  # Adiciona um icon de lixeira
        button_deleteTask.setToolTip('Delete Task')
        button_deleteTask.setCursor(Qt.PointingHandCursor)
        button_deleteTask.setStyleSheet("border: 0;")
        button_deleteTask.clicked.connect(self._deleteTask)

        # Adciona os widgets na grid
        grid.addWidget(self._task, 0, 0)
        grid.addWidget(self.checkBoxItem, 0, 1)
        grid.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 2)  # Espaço vazio
        grid.addWidget(button_deleteTask, 0, 3)

        # Insere a grid no atributo widget
        self.widget.setLayout(grid)

        # Define o tamanho do widget com base no tamanho sugerido pelo layout
        self.setSizeHint(self.widget.sizeHint())

    def _concludeTask(self):
        """Método que atualiza visualmente a mensagem da tarefa, rasurando-a ou desrasurando-a."""

        # Verifica o estado da checkBoxItem
        if self.checkBoxItem.isChecked():
            self._task.setText(''.join([c + '\u0336' for c in self._task.text()]))  # Resuara a menssagem da tarefa
        else:
            self._task.setText(''.join(c for c in self._task.text() if unicodedata.combining(c) == 0))  # Desrasura

    def _deleteTask(self):
        """Método responsável por deletar a tarefa"""

        # Retira o item da lista que está setado
        self.listWidget().takeItem(self.listWidget().row(self))

        # Deleta o item do Bnaco de dados
        self._db.deleteTask(self.data(Qt.UserRole))


class TaskDataBasse(QSqlDatabase):
    """Banco de dados onde estão todas as tarefas"""

    def __init__(self):
        """
        Configura o banco de dados

        Raises:
            Exception: Caso não seja possível abrir o banco de dados
        """

        # Chama o construtor da classe pai para inicializar a instância
        super().__init__()

        # Configura o banco de dados como SQLITE
        self.addDatabase(QSqlDatabase.drivers()[0])

        # Atribui um nome para o database
        self.database().setDatabaseName('tasks.db')

        if not self.database().open():
            raise Exception('Erro ao tentar abrir o banco de dados.')

        # Define um Query
        self._query = QSqlQuery(self.database())

        # Cria a tabela para as tarefas, se não existir
        self._query.exec_("""
            CREATE TABLE IF NOT EXISTS tasks (
                task VARCHAR(50) NOT NULL,
                checked_task BOOLEAN NOT NULL CHECK (checked_task IN (0, 1)),
                id_task INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL
            );
        """)

    def addTask(self, menssage_task: str):
        """
        Adiciona uma nova tarefa ao banco de dados

        Args:
            menssage_task (str): Texto da nova task
        """

        # Consulta preparada para inserir uma nova tarefa
        self._query.prepare('INSERT INTO tasks (task, checked_task) VALUES (:task, :checked_task)')
        self._query.bindValue(':task', menssage_task)
        self._query.bindValue(':checked_task', 0)  # Inicializa com valor não marcado
        self._query.exec_()

    def deleteTask(self, id_task: int):
        """
        Exclui uma task do banco de dados

        Args:
            id_task (int): ID da tarefa que será excluída
        """

        # Consulta preparada para excluir uma tarefa com base no ID
        self._query.prepare('DELETE FROM tasks WHERE id_task = :id_task')
        self._query.bindValue(':id_task', id_task)
        self._query.exec_()

    def changeStateChecked(self, id_task: int):
        """
        Altera o valor checked de True (1) para False (0) ou vice-versa

        Args:
            id_task (int): ID da task que terá o valor checked modificado
        """

        # Consulta preparada para obter o valor atual de checked_task para a tarefa específica
        self._query.prepare('SELECT checked_task FROM tasks WHERE id_task = :id_task')
        self._query.bindValue(':id_task', id_task)
        self._query.exec_()
        self._query.next()
        checked_task = self._query.value(0)

        # Consulta preparada para atualizar o estado de checked_task
        self._query.prepare('UPDATE tasks SET checked_task = :new_state WHERE id_task = :id_task')
        self._query.bindValue(':id_task', id_task)
        self._query.bindValue(':new_state', 0 if checked_task else 1)  # Inverte o estado atual
        self._query.exec_()

    def getTasks(self) -> list:
        """
        Obtém todas as tasks registradas no banco de dados

        Returns:
            list: Lista com tuplas, que contêm, em ordem decrescente, as informações das tarefas (texto, checked, id)
        """

        # Define a lista com as tarefas
        tasks = []

        # Consulta para obter todas as tarefas ordenadas por ID de forma decrescente
        self._query.exec_('SELECT * FROM tasks ORDER BY id_task DESC')

        # Preenche a lista com as tuplas de informações das tarefas
        while self._query.next():
            tasks.append((self._query.value(0), self._query.value(1), self._query.value(2)))

        return tasks
