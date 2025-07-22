import os
import googlemaps
from datetime import datetime

# Inicializa o cliente Google Maps com a API_KEY do ambiente (Render)
gmaps = googlemaps.Client(key=os.environ["API_KEY"])

def buscar_place_id(query):
    """Busca o place_id de uma estação usando Google Places Autocomplete."""
    tentativa = f"Estação {query}, São Paulo, SP"
    try:
        resultados = gmaps.places_autocomplete(
            input_text=tentativa,
            components={"country": "br"}
        )
        if resultados:
            return f"place_id:{resultados[0]['place_id']}"
    except Exception as e:
        print(f"[ERRO buscar_place_id]: {e}")

    return query  # fallback textual simples

def interpretar_passo(passo):
    """Converte um passo da rota em linguagem natural, se for transporte público."""
    try:
        if 'transit_details' in passo:
            detalhes = passo['transit_details']
            origem = detalhes['departure_stop']['name']
            destino = detalhes['arrival_stop']['name']
            linha = detalhes['line'].get('short_name') or detalhes['line'].get('name')
            sentido = detalhes['headsign']
            return f"Pegue a linha {linha} na estação {origem}, sentido {sentido}, e desça na estação {destino}."
    except Exception as e:
        print(f"[ERRO interpretar_passo]: {e}")
    return None

def consultar_rota_google(origem_texto, destino_texto):
    """
    Consulta a rota entre duas estações via Google Directions API (transporte ferroviário).
    Retorna instruções em texto ou None se não houver rota.
    """
    try:
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

    except Exception as e:
        print(f"[ERRO consultar_rota_google]: {e}")

    return None  # Fallback: deixa o `duvidas.py` usar a Anthropic
