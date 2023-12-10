# TaskList

 ### Descrição do projeto
  Este projeto [python](https://python.org) consiste em uma aplicação de lista de tarefas (to-do list) com uma interface gráfica [PyQt5](https://pypi.org/project/PyQt5/) e um banco de dados [SQLite](https://www.sqlite.org/index.html) para armazenar as tarefas. A aplicação permite adicionar, concluir e excluir tarefas. Sendo que o projeto está dividido em três códigos .py:
  - [main.py](/Scripts-py/main.py): O script de inicialização do projeto, ou seja, exibe a interface gráfica e inicia o loop de execução da aplicação.
  - [interface.py](/Scripts-py/interface.py): Define a classe `TaskListInterface`, que herda de `QWidget` e representa a interface gráfica da lista de tarefas.
  - [tools.py](/Scripts-py/tools.py): Contém funcionalidades complementares para a interface, incluindo as classes `TaskItem` e `TaskDataBasse`. Sendo a primeira uma subclasse de `QListWidgetItem` que representa uma tarefa na lista, possuindo métodos para concluir e excluir tarefas. Já `TaskDataBasse` é uma subclasse de `QSqlDatabase` que gerencia/manipula o banco de dados SQLite do projeto, `tasks.db`, que será criado assim que é feita a execução do programa.

 ### Requisitos
  * [Python](https://www.python.org/downloads/)
  
  * *IDE* - Algumas sugestões:
   
      1. [PyCharm](https://www.jetbrains.com/pt-br/pycharm/)
      2. [Visal Studio Code](https://code.visualstudio.com/)
      3. [Jupyter](https://jupyter.org/)

 ### Como usar?
  - Com o Python e a *IDE* instalados, o próximo passo é incorporar os três arquivos .py, localizados na pasta [Scripts-py](/Scripts-py), ao seu projeto na *IDE*. Em seguida, no terminal do compilador, execute os seguintes comandos:
  
     ```
     pip install PyQt5
     ```
  
     ```
     pip install qtawesome
     ```
  
     ```
     pip install unicodedata
     ```
 
  - Após a instalação, abra o arquivo [main.py](/Scripts-py/main.py) e execute-o. Assim a interface gráfica será exibida com um campo de entrada para adicionar novas tarefas. Digite uma tarefa no campo de entrada e clique no botão "Add task" para adicioná-la à lista. Cada tarefa na lista, `TaskItem`, possui uma caixa de seleção para marcar como concluída (ou não) e um botão de exclusão (representado pelo ícone de lixeira) para remover a tarefa.

 ### Observações
  - As tarefas são exibidas em ordem decrescente de criação, ou seja, da mais recente à mais antiga.
  - Clique na caixa de seleção de uma tarefa para marcá-la como concluída (ou desmarque para indicar que não está concluída). Dessa forma, o texto associado à tarefa será rasurado (ou retornado ao estado original).
  - Clique no botão de exclusão para remover uma tarefa da lista.
  - **Este projeto, por ser projetado para ser simples, não inclui algumas funcionalidades, como a separação de tarefas por categorias.**
  - **A aplicação possui alguns erros, principalmente visuais.**
