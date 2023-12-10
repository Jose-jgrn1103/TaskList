"""Script da interface da lista de tarefas"""

from PyQt5.QtCore import Qt
from tools import TaskItem, TaskDataBasse
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QListWidget


class TaskListInterface(QWidget):
    """Classe da interface da Task List"""

    # Atributo do visual da janela
    _VISUAL = """
            /*Visual do rótulo de título*/
            #title{
                margin-top: 50px;
                margin-bottom: 30px;
                                
                font: 50px Lucida Handwriting;
            }
            
            /*Visual da entrada de tarefas*/
            #input-task{
                margin-bottom: 20px;
                padding: 10px;
                
                border: 1px solid #4682B4;
                border-radius: 20%;
                
                font: 28px Arial;
            }
            #input-task::hover{
                border-width: 2px;
            }
            
            /*Visual da entrada de tarefas quando dá erro*/
            #input-task-error{
                margin-bottom: 20px;
                padding: 10px;
                
                border: 1px solid red;
                border-radius: 20%;
                
                font: 28px Arial;
            }
            #input-task-error::hover{
                border-width: 2px;
            }
            
            /*Visual do botão de adicionar tarefa*/
            #button-addtask{
                margin: 0 60px;
                padding: 15px;
                
                background-color: #1E90FF;
                
                border-radius: 20%;
                
                font: 30px Arial;
                color: white;
            }
            #button-addtask::hover{
                background-color: #1876D1;
            }
            #button-addtask::pressed{
                background-color: #1E90FF;
            }
            
            /*Visual da lista de tarefas*/
            #list-tasks{
                margin-top: 20px;
                border: 1px solid #4682B4;
            }
    """

    # Atributo que cria uma conecxão com o banco de dados das tasks
    _DATABASE = TaskDataBasse()

    def __init__(self):
        """Inicializa e configura a instância de TaskListInterface"""

        # Chama o construtor da classe pai (QMainWindow) e Define o tamanho da interface para ocupar toda a tela
        super().__init__()
        self.showMaximized()

        # Atribui um estilo e um título na janela
        self.setStyleSheet(self._VISUAL)
        self.setWindowTitle('Task List')

        # Chama o método _initComponents() para istanciar os widgets na interface
        self._initComponents()

    def _initComponents(self):
        """Método responsável por dispor os elemento na janela"""

        # Define e aplica na interface uma grid
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Cria um rótulo para o título
        title = QLabel('Task List')
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName('title')

        # Gera um input para a tarefa ser digitada
        self._inputTask = QLineEdit()
        self._inputTask.setMaxLength(50)  # Define um limite de 50 caracteres
        self._inputTask.setPlaceholderText('Enter a task')
        self._inputTask.setObjectName('input-task')

        # Define um butão para acrescentar a tarefa
        button_addTask = QPushButton('Add task')
        button_addTask.setCursor(Qt.PointingHandCursor)
        button_addTask.clicked.connect(self.addTask)
        button_addTask.setObjectName('button-addtask')

        # Cria a lista de tarefas
        self._listTasks = QListWidget()
        self._addTasksinList()
        self._listTasks.setObjectName('list-tasks')

        # Adciona todos os widgets na grid
        grid_layout.addWidget(title, 0, 0)
        grid_layout.addWidget(self._inputTask, 1, 0)
        grid_layout.addWidget(button_addTask, 2, 0)
        grid_layout.addWidget(self._listTasks, 3, 0)

    def _addTasksinList(self):
        """Método responsável por adcionar as tarefas do _DATABASE na _listTasks"""

        # Limpa a lista de tarefas
        self._listTasks.clear()

        # Itera sobre as tasks obtidas do banco de dados
        for items in self._DATABASE.getTasks():
            # Define o item e seu id
            item = TaskItem(items[0], self._DATABASE)
            item.setData(Qt.UserRole, items[2])

            # Verifica se o item foi conclído, caso seja verdade ativa o check_box dele
            if items[1]:
                item.checkBoxItem.setChecked(True)

            # Adciona o item na lista de tarefas
            self._listTasks.addItem(item)
            self._listTasks.setItemWidget(item, item.widget)

    def addTask(self):
        """Método que adciona uma nova nota de tarefa com base no texto do _inputTask"""

        # Checa se o texto do _inputTask não está vazio
        if menssage_task := self._inputTask.text():
            # Limpa a entrada
            self._inputTask.clear()

            # Retorna o placeholder e o nome para o padrão
            self._inputTask.setPlaceholderText('Enter a task')
            self._inputTask.setObjectName('input-task')

            # Adciona a tarefa digitada no data base e atualiza a lista com  _addTasksinList()
            self._DATABASE.addTask(menssage_task)
            self._addTasksinList()
        else:
            # Altera o placeholder da entrada e seu nome
            self._inputTask.setPlaceholderText('Empty input')
            self._inputTask.setObjectName('input-task-error')

        # Atualiza o estilo da tela
        self.setStyleSheet(self._VISUAL)
