from pathlib import Path

from src.controller.maluquice import run_agents_test

def test_agents():
    """
    Rota de teste para executar todos os agentes.
    """

    dxf_path = r"C:\Users\wmdna\OneDrive\Documentos\EchoCAD\app\backend\uploads\PNR S Ten Sgt - 2ª Fase.dxf"  #colar endereco

    if not Path(dxf_path).exists():
        ...

    result = run_agents_test(dxf_path)

    return result


if __name__ == "__main__":
    resultado  = test_agents()
    print(resultado)
