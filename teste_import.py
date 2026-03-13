import sys
import os

# Força o Python a esquecer qualquer 'app' que ele conheça
if 'app' in sys.modules:
    del sys.modules['app']

# Garante que o diretório atual está no topo da busca
sys.path.insert(0, os.getcwd())

try:
    # Tenta importar o módulo diretamente pelo caminho do arquivo
    import importlib.util
    spec = importlib.util.spec_from_file_location("repository_redis", "app/repositories/repository_redis.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    
    print("✅ Arquivo lido com sucesso!")
    print("Funções encontradas:", [f for f in dir(foo) if not f.startswith('__')])
    
    if hasattr(foo, 'get_session_and_history'):
        print("🚀 A função EXISTE no arquivo!")
    else:
        print("❌ A função NÃO FOI ENCONTRADA dentro do arquivo. Verifique o nome dela no código.")

except Exception as e:
    print(f"💥 Erro ao ler o arquivo: {e}")