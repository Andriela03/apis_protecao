import requests
from requests.exceptions import ConnectionError

# ==========================================
# CONFIGURAÇÃO
# ==========================================

url = "http://127.0.0.1:5000/hello"

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def verificar(condicao, sucesso, erro):
    if condicao:
        print(f"✔ {sucesso}")
    else:
        print(f"✘ {erro}")


def exibir_resposta(response):

    print(f"Status recebido: {response.status_code}")

    print("\nCabeçalhos da resposta:")

    if response.headers:
        for chave, valor in response.headers.items():
            print(f"{chave}: {valor}")
    else:
        print("Nenhum cabeçalho encontrado.")

    print("\nCorpo da resposta:")
    print(response.text)


# ==========================================
# TESTE 1
# REQUISIÇÃO SEM AUTENTICAÇÃO
# ==========================================

print("=" * 60)
print("TESTE 1 - ACESSO SEM AUTENTICAÇÃO")
print("=" * 60)

try:

    response = requests.get(url)

    exibir_resposta(response)

    www_auth = response.headers.get("WWW-Authenticate")

    print("\nValidações:")

    verificar(
        response.status_code == 401,
        "Status 401 Unauthorized recebido corretamente",
        f"Status inesperado ({response.status_code})"
    )

    verificar(
        response.request.path_url == "/hello",
        "Recurso /hello acessado corretamente",
        f"Recurso inesperado ({response.request.path_url})"
    )

    verificar(
        www_auth is not None,
        "Cabeçalho WWW-Authenticate encontrado",
        "Cabeçalho WWW-Authenticate ausente"
    )

    verificar(
        www_auth is not None and "Basic" in www_auth,
        "Estratégia Basic identificada",
        "Estratégia Basic não encontrada"
    )

    verificar(
        www_auth is not None and 'realm="Authentication Required"' in www_auth,
        "Realm padrão identificado",
        "Realm inesperado"
    )

except ConnectionError:

    print("✘ Não foi possível conectar à API.")

except Exception as erro:

    print(f"✘ Erro inesperado: {erro}")


# ==========================================
# TESTE 2
# REQUISIÇÃO COM BASIC AUTH
# ==========================================

print("\n\n" + "=" * 60)
print("TESTE 2 - ACESSO COM BASIC AUTH")
print("=" * 60)

try:

    response = requests.get(
        url,
        auth=("admin", "123")
    )

    exibir_resposta(response)

    authorization = response.request.headers.get("Authorization")

    print("\nValidações:")

    verificar(
        response.status_code == 200,
        "Status 200 OK recebido corretamente",
        f"Status inesperado ({response.status_code})"
    )

    verificar(
        response.request.path_url == "/hello",
        "Recurso /hello acessado corretamente",
        f"Recurso inesperado ({response.request.path_url})"
    )

    verificar(
        authorization is not None,
        "Cabeçalho Authorization enviado",
        "Cabeçalho Authorization não enviado"
    )

    verificar(
        authorization is not None and authorization.startswith("Basic "),
        "Cabeçalho Basic enviado corretamente",
        "Cabeçalho Authorization não utiliza Basic"
    )

    if authorization:
        print("\nAuthorization enviado:")
        print(authorization)

except ConnectionError:

    print("✘ Não foi possível conectar à API.")

except Exception as erro:

    print(f"✘ Erro inesperado: {erro}")


# ==========================================
# RESUMO
# ==========================================

print("\n\n" + "=" * 60)
print("FIM DOS TESTES")
print("=" * 60)