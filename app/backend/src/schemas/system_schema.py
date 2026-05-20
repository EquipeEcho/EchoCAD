from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """
    Schema para resposta de upload bem sucedido.
    """

    message: str
    filename: str
    path: str


# schema genérico para indicar sucesso na criação de objetos.
class Success(BaseModel):
    """
    Schema para resposta de sucesso na criação de objetos.
    """

    object: str
    message: str
