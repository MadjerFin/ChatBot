import os
import googlemaps
from datetime import datetime

# Usa diretamente a variável de ambiente configurada no Render
gmaps = googlemaps.Client(key=os.environ["API_KEY"])

def buscar_place_id(query):
    tentativa = f"Estação {query}, São Paulo, SP"
    resultados = gmaps.places_autocomplete(
        input_text=tentativa,
        components={"country": "br"}
    )

    if resultados:
        return f"place_id:{resultados[0]['place_id']}"
    return tentativa  # fallback textual

def interpretar_passo(passo):
    if 'transit_details' in passo:
        detalhes = passo['transit_details']
        origem = detalhes['departure_stop']['name']
        destino = detalhes['arrival_stop']['name']
        linha = detalhes['line'].get('short_name') or detalhes['line'].get('name')
        sentido = detalhes['headsign']
        return f"Pegue a linha {linha} na estação {origem}, sentido {sentido}, e desça na estação {destino}."
    return None

def consultar_rota_google(origem_texto, destino_texto):
    origem = buscar_place_id(origem_texto)
    destino = buscar_place_id(destino_texto)

    rota = gmaps.directions(
        origem,
        destino,
        mode="transit",
        transit_mode="rail",
        language="pt-BR",
        departure_time=datetime.now()
    )

    if rota:
        passos = []
        for passo in rota[0]['legs'][0]['steps']:
            frase = interpretar_passo(passo)
            if frase:
                passos.append(frase)
        if passos:
            return "\n".join(f"{i+1}. {p}" for i, p in enumerate(passos))
    return None
