#!/usr/bin/env python3
"""
Script para resetar o banco de dados EchoCAD.
Este script:
1. Cria o banco e usuário se não existirem
2. Remove todas as tabelas existentes
3. Configura as permissões corretas
"""

import sys
import pymysql
from urllib.parse import urlparse
import os
import getpass

# Adicionar o diretório src ao path para importar config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import settings


def parse_database_url(url):
    """Parse database URL to extract components."""
    parsed = urlparse(url)
    return {
        'host': parsed.hostname,
        'port': parsed.port or 3306,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/')
    }


def create_database_and_user(admin_host, admin_user, admin_password, target_db, target_user, target_password):
    """Create database and user if they don't exist."""
    try:
        # Connect without specifying database
        connection = pymysql.connect(
            host=admin_host,
            user=admin_user,
            password=admin_password,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{target_db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Banco de dados '{target_db}' criado/verificado")

            # Create user if not exists
            cursor.execute(f"CREATE USER IF NOT EXISTS '{target_user}'@'%' IDENTIFIED BY '{target_password}'")
            print(f"✓ Usuário '{target_user}' criado/verificado")

            # Grant all privileges except DROP DATABASE
            cursor.execute(f"""
                GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, REFERENCES, CREATE TEMPORARY TABLES,
                       LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER
                ON `{target_db}`.* TO '{target_user}'@'%'
            """)
            print(f"✓ Privilégios concedidos ao usuário '{target_user}' no banco '{target_db}'")

            # Flush privileges
            cursor.execute("FLUSH PRIVILEGES")
            print("✓ Privilégios atualizados")

        connection.commit()

    except pymysql.Error as e:
        print(f"✗ Erro ao criar banco/usuário: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

    return True


def drop_all_tables(admin_host, admin_user, admin_password, target_db):
    """Drop all tables in the database using admin credentials."""
    try:
        connection = pymysql.connect(
            host=admin_host,
            user=admin_user,
            password=admin_password,
            database=target_db,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            if not tables:
                print("✓ Nenhuma tabela encontrada para remover")
                return True

            # Disable foreign key checks to allow dropping tables with constraints
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Drop all tables
            dropped_count = 0
            for table in tables:
                table_name = list(table.values())[0]
                try:
                    cursor.execute(f"DROP TABLE `{table_name}`")
                    print(f"✓ Tabela '{table_name}' removida")
                    dropped_count += 1
                except pymysql.Error as e:
                    if "Unknown table" in str(e):
                        print(f"⚠ Tabela '{table_name}' já foi removida (possivelmente por CASCADE)")
                    else:
                        print(f"✗ Erro ao remover tabela '{table_name}': {e}")

            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        connection.commit()
        print(f"✓ {dropped_count} tabelas foram removidas com sucesso")

    except pymysql.Error as e:
        print(f"✗ Erro ao remover tabelas: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

    return True


def main():
    """Main function."""
    print("🔄 Iniciando reset do banco de dados EchoCAD...")

    # Parse database URL from config
    db_config = parse_database_url(settings.database_url)
    print(f"📍 Configuração do banco: {db_config['host']}:{db_config['port']}/{db_config['database']}")

    # Admin credentials
    admin_user = input("Digite o usuário admin do MySQL (default: root): ").strip() or "root"
    admin_password = getpass.getpass("Digite a senha do admin do MySQL: ")

    if not admin_password:
        print("✗ Senha do admin é obrigatória")
        return 1

    # Target credentials
    target_user = "echocad_admin"
    target_password = "echocad_admin_password"
    target_db = db_config['database']

    print(f"👤 Usuário alvo: {target_user}")
    print(f"🗄️ Banco alvo: {target_db}")

    # Step 1: Create database and user
    print("\n1. Criando banco e usuário...")
    if not create_database_and_user(db_config['host'], admin_user, admin_password, target_db, target_user, target_password):
        return 1

    # Step 2: Drop all tables using admin credentials
    print("\n2. Removendo todas as tabelas...")
    if not drop_all_tables(db_config['host'], admin_user, admin_password, target_db):
        return 1

    print("\n✅ Reset do banco de dados concluído com sucesso!")
    print("📋 O banco está agora limpo e pronto para novas migrações.")
    return 0


if __name__ == "__main__":
    sys.exit(main())