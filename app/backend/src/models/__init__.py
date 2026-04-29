from .file_cad import FileCad
from .database.usuario import Usuario
from .database.projeto import Projeto
from .database.norma import Norma
from .database.projeto_norma import ProjetoNorma
from .database.planta_cad import PlantaCad
from .database.projeto_planta import ProjetoPlanta
from .database.especificacoes_tecnicas import EspecificacaoTecnica
from .database.memoriais_calculo import MemorialCalculo

# Backward compatibility aliases for old names
User = Usuario
Project = Projeto