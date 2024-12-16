import requests

# Configuración
GITHUB_TOKEN = "token"  # Reemplaza con tu token personal
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
USUARIO_OBJETIVO = "mgeovany"

# Consulta GraphQL
GRAPHQL_QUERY = """
{
  user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""

def obtener_usuarios_honduras():
    """Obtiene usuarios con ubicación en Honduras usando la API REST."""
    url = "https://api.github.com/search/users?q=location:Honduras"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return [user["login"] for user in response.json().get("items", [])]
    else:
        print("Error al obtener usuarios:", response.status_code, response.text)
        return []

def obtener_contribuciones(usuario):
    """Obtiene el total de contribuciones (públicas y privadas) usando GraphQL."""
    url = "https://api.github.com/graphql"
    query = GRAPHQL_QUERY % usuario
    response = requests.post(url, json={"query": query}, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return (data.get("data", {})
                    .get("user", {})
                    .get("contributionsCollection", {})
                    .get("contributionCalendar", {})
                    .get("totalContributions", 0))
    else:
        print(f"Error al obtener contribuciones de {usuario}: {response.text}")
        return 0

def main():
    print("Obteniendo usuarios de Honduras...")
    usuarios = obtener_usuarios_honduras()
    if not usuarios:
        print("No se encontraron usuarios.")
        return

    contribuciones = []
    print("\nCalculando contribuciones...")
    
    # Obtener contribuciones solo para los usuarios en la lista
    for usuario in usuarios:
        total = obtener_contribuciones(usuario)
        contribuciones.append({"usuario": usuario, "contributions": total})

    # Agregar el usuario objetivo si no está en la lista
    if USUARIO_OBJETIVO not in [u["usuario"] for u in contribuciones]:
        print(f"Agregando contribuciones para {USUARIO_OBJETIVO}...")
        total_objetivo = obtener_contribuciones(USUARIO_OBJETIVO)
        contribuciones.append({"usuario": USUARIO_OBJETIVO, "contributions": total_objetivo})

    # Ordenar por contribuciones (mayor a menor)
    contribuciones = sorted(contribuciones, key=lambda x: x["contributions"], reverse=True)

    # Mostrar solo el Top 3
    print("\n🎉 Top 3 de contribuyentes en Honduras 🎉")
    for idx, user in enumerate(contribuciones[:3], start=1):
        print(f"Top {idx}: {user['usuario']} - {user['contributions']} contribuciones")

    # Mostrar la posición del usuario objetivo
    for idx, user in enumerate(contribuciones, start=1):
        if user["usuario"] == USUARIO_OBJETIVO:
            print(f"\n🎯 ¡{USUARIO_OBJETIVO} está en la posición {idx} con {user['contributions']} contribuciones! 🎯")
            break

if __name__ == "__main__":
    main()
