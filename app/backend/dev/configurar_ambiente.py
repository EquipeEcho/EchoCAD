#!/usr/bin/env python3
"""
Script para configurar o ambiente de desenvolvimento EchoCAD.
Este script:
1. Instala/atualiza pipx
2. Instala/atualiza uv via pipx
3. Executa uv sync para configurar dependências
4. Fornece instruções finais para VS Code
"""

import subprocess
import sys
import os
import platform
import urllib.request
import json


def run_command(command, shell=True, capture_output=True, check=True):
    """Executa um comando e retorna o resultado."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao executar comando: {command}")
        print(f"Erro: {e}")
        return None


def is_windows():
    """Verifica se está executando no Windows."""
    return platform.system() == "Windows"


def check_command_exists(command):
    """Verifica se um comando está disponível no PATH."""
    try:
        if is_windows():
            result = run_command(f"where {command}", check=False)
        else:
            result = run_command(f"which {command}", check=False)
        return result and result.returncode == 0
    except:
        return False


def get_latest_version_pipx():
    """Obtém a versão mais recente do pipx do PyPI."""
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/pipx/json", timeout=10) as response:
            data = json.loads(response.read())
            return data["info"]["version"]
    except:
        return None


def get_current_version_pipx():
    """Obtém a versão atual do pipx instalado."""
    try:
        result = run_command("pipx --version", check=False)
        if result and result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None


def install_or_update_pipx():
    """Instala ou atualiza o pipx."""
    print("\n🔧 Verificando pipx...")

    # Verifica se pipx está instalado
    pipx_installed = check_command_exists("pipx")
    current_version = get_current_version_pipx() if pipx_installed else None

    if pipx_installed and current_version:
        print(f"✓ pipx encontrado (versão: {current_version})")

        # Verifica versão mais recente
        latest_version = get_latest_version_pipx()
        if latest_version and current_version != latest_version:
            print(f"📦 Versão mais recente disponível: {latest_version}")
            update = input("Deseja atualizar pipx? (s/n): ").lower().strip()
            if update == 's':
                print("🔄 Atualizando pipx...")
                result = run_command("python -m pip install --upgrade pipx")
                if result and result.returncode == 0:
                    print("✓ pipx atualizado com sucesso!")
                    # Refresh PATH no Windows
                    if is_windows():
                        run_command("refreshenv", check=False)
                    return True
                else:
                    print("✗ Falha ao atualizar pipx")
                    return False
            else:
                print("⏭️ Continuando com versão atual...")
                return True
        else:
            print("✓ pipx já está na versão mais recente")
            return True
    else:
        print("📦 pipx não encontrado")
        install = input("Deseja instalar pipx? (s/n): ").lower().strip()
        if install == 's':
            print("🔄 Instalando pipx...")
            result = run_command("python -m pip install pipx")
            if result and result.returncode == 0:
                # Inicializar pipx
                run_command("pipx ensurepath", check=False)
                # Refresh PATH no Windows
                if is_windows():
                    run_command("refreshenv", check=False)
                print("✓ pipx instalado com sucesso!")
                return True
            else:
                print("✗ Falha ao instalar pipx")
                return False
        else:
            print("❌ pipx é necessário. Saindo...")
            return False


def get_latest_version_uv():
    """Obtém a versão mais recente do uv do GitHub."""
    try:
        with urllib.request.urlopen("https://api.github.com/repos/astral-sh/uv/releases/latest", timeout=10) as response:
            data = json.loads(response.read())
            return data["tag_name"].lstrip('v')
    except:
        return None


def get_current_version_uv():
    """Obtém a versão atual do uv instalado."""
    try:
        result = run_command("uv --version", check=False)
        if result and result.returncode == 0:
            # uv --version retorna algo como "uv 0.1.0"
            version = result.stdout.strip().split()[-1]
            return version
    except:
        pass
    return None


def install_or_update_uv():
    """Instala ou atualiza o uv via pipx."""
    print("\n🔧 Verificando uv...")

    # Verifica se uv está instalado
    uv_installed = check_command_exists("uv")
    current_version = get_current_version_uv() if uv_installed else None

    if uv_installed and current_version:
        print(f"✓ uv encontrado (versão: {current_version})")

        # Verifica versão mais recente
        latest_version = get_latest_version_uv()
        if latest_version and current_version != latest_version:
            print(f"📦 Versão mais recente disponível: {latest_version}")
            update = input("Deseja atualizar uv? (s/n): ").lower().strip()
            if update == 's':
                print("🔄 Tentando atualizar uv...")
                # Tenta upgrade primeiro
                result = run_command("pipx upgrade uv", check=False)
                if result and result.returncode == 0:
                    print("✓ uv atualizado com sucesso!")
                    return True

                # Se upgrade falhar, tenta reinstalar
                print("⚠️ Upgrade falhou, tentando reinstalar...")
                result = run_command("pipx install --force uv", check=False)
                if result and result.returncode == 0:
                    print("✓ uv reinstalado com sucesso!")
                    return True

                # Se tudo falhar, informa ao usuário
                print("⚠️ Não foi possível atualizar automaticamente o uv.")
                print("💡 Você pode atualizar manualmente executando:")
                print("   pipx install --force uv")
                print("   ou")
                print("   pipx uninstall uv && pipx install uv")
                continue_anyway = input("Continuar com a versão atual? (s/n): ").lower().strip()
                if continue_anyway == 's':
                    return True
                else:
                    return False
            else:
                print("⏭️ Continuando com versão atual...")
                return True
        else:
            print("✓ uv já está na versão mais recente")
            return True
    else:
        print("📦 uv não encontrado")
        install = input("Deseja instalar uv? (s/n): ").lower().strip()
        if install == 's':
            print("🔄 Instalando uv...")
            result = run_command("pipx install uv")
            if result and result.returncode == 0:
                print("✓ uv instalado com sucesso!")
                return True
            else:
                print("✗ Falha ao instalar uv via pipx")
                print("💡 Tente instalar manualmente:")
                print("   pipx install uv")
                return False
        else:
            print("❌ uv é necessário. Saindo...")
            return False


def run_uv_sync():
    """Executa uv sync na pasta src."""
    print("\n🔧 Executando uv sync...")

    # Muda para o diretório src
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
    os.chdir(src_dir)

    print(f"📁 Executando em: {os.getcwd()}")

    result = run_command("uv sync")
    if result and result.returncode == 0:
        print("✓ uv sync executado com sucesso!")
        return True
    else:
        print("✗ Falha ao executar uv sync")
        return False


def show_final_instructions():
    """Mostra instruções finais para o usuário."""
    print("\n" + "="*60)
    print("🎉 AMBIENTE CONFIGURADO COM SUCESSO!")
    print("="*60)

    # Calcula o caminho do venv de forma relativa ao script
    script_dir = os.path.dirname(__file__)
    venv_path = os.path.abspath(os.path.join(script_dir, '..', 'src', '.venv'))

    print("\n📋 PRÓXIMOS PASSOS - CONFIGURAÇÃO DO VS CODE:")
    print(f"1. Abra o VS Code no diretório do projeto")
    print(f"2. Pressione Ctrl+Shift+P (ou Cmd+Shift+P no Mac)")
    print(f"3. Digite 'Python: Select Interpreter' e selecione")
    print(f"4. Escolha o interpretador: '{venv_path}'")
    print(f"5. Ou configure no settings.json:")
    print(f'   "python.defaultInterpreterPath": "{venv_path}"')

    print("\n🔧 COMANDOS ÚTEIS:")
    print("• Executar aplicação: uv run fastapi dev main.py")
    print("• Executar testes: uv run pytest")
    print("• Gerenciar dependências: uv add/remove [pacote]")
    print("• Reset banco: uv run python dev/reset_database.py")

    print("\n✨ Ambiente pronto para desenvolvimento!")


def main():
    """Função principal."""
    print("🚀 Configurando ambiente de desenvolvimento EchoCAD...")

    if not is_windows():
        print("⚠️ Este script foi otimizado para Windows. Continuando mesmo assim...")

    # Verifica se Python está disponível
    if not check_command_exists("python"):
        print("❌ Python não encontrado. Instale o Python primeiro.")
        return 1

    # Passo 1: pipx
    if not install_or_update_pipx():
        return 1

    # Passo 2: uv
    if not install_or_update_uv():
        return 1

    # Passo 3: uv sync
    if not run_uv_sync():
        return 1

    # Instruções finais
    show_final_instructions()

    return 0


if __name__ == "__main__":
    sys.exit(main())