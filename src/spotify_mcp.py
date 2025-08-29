import os
import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

load_dotenv()

ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN')

def get_active_device():
    """Obtiene el dispositivo activo de Spotify"""
    if not ACCESS_TOKEN:
        return None
        
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://api.spotify.com/v1/me/player/devices', headers=headers, timeout=10)
        
        if response.status_code == 200:
            devices = response.json()['devices']
            for device in devices:
                if device.get('is_active'):
                    return device['id']
            return None
        else:
            return None
    except Exception:
        return None

def next_track():
    """Saltar a la siguiente canción en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        device_id = get_active_device()
        if not device_id:
            return {"success": False, "error": "No hay dispositivo activo encontrado"}
        
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Hacer request a next track
        response = requests.post(
            f'https://api.spotify.com/v1/me/player/next?device_id={device_id}', 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:  # 200 es el código correcto
            return {"success": True, "action": "next_track", "device_id": device_id}
        elif response.status_code == 403:
            return {"success": False, "error": "Token expirado o permisos insuficientes"}
        elif response.status_code == 404:
            return {"success": False, "error": "No hay dispositivos activos"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

def previous_track():
    """Ir a la canción anterior en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        device_id = get_active_device()
        if not device_id:
            return {"success": False, "error": "No hay dispositivo activo encontrado"}
        
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Hacer request a previous track
        response = requests.post(
            f'https://api.spotify.com/v1/me/player/previous?device_id={device_id}', 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 204:  # 204 es el código correcto
            return {"success": True, "action": "previous_track", "device_id": device_id}
        elif response.status_code == 403:
            return {"success": False, "error": "Token expirado o permisos insuficientes"}
        elif response.status_code == 404:
            return {"success": False, "error": "No hay dispositivos activos"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

def pause_track():
    """Pausar la reproducción en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        device_id = get_active_device()
        if not device_id:
            return {"success": False, "error": "No hay dispositivo activo encontrado"}
        
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Hacer request a pause
        response = requests.put(
            f'https://api.spotify.com/v1/me/player/pause?device_id={device_id}', 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 204:  # 204 es el código correcto
            return {"success": True, "action": "pause", "device_id": device_id}
        elif response.status_code == 403:
            return {"success": False, "error": "Token expirado o permisos insuficientes"}
        elif response.status_code == 404:
            return {"success": False, "error": "No hay dispositivos activos"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

def resume_track():
    """Reanudar la reproducción en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        device_id = get_active_device()
        if not device_id:
            return {"success": False, "error": "No hay dispositivo activo encontrado"}
        
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Hacer request a play/resume
        response = requests.put(
            f'https://api.spotify.com/v1/me/player/play?device_id={device_id}', 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 204:  # 204 es el código correcto
            return {"success": True, "action": "resume", "device_id": device_id}
        elif response.status_code == 403:
            return {"success": False, "error": "Token expirado o permisos insuficientes"}
        elif response.status_code == 404:
            return {"success": False, "error": "No hay dispositivos activos"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

def current_track():
    """Obtener información de la canción que se está reproduciendo actualmente"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    try:
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.get(
            'https://api.spotify.com/v1/me/player/currently-playing',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data and 'item' in data and data['item']:
                track = data['item']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                track_name = track['name']
                album_name = track['album']['name']
                is_playing = data.get('is_playing', False)
                duration_ms = track.get('duration_ms', 0)
                return {
                    "success": True,
                    "track": track_name,
                    "artist": artists,
                    "album": album_name,
                    "status": "Reproduciendo" if is_playing else "Pausado",
                    "duration": f"{duration_ms // 60000}:{(duration_ms % 60000) // 1000:02d}"
                }
            else:
                return {
                    "success": False,
                    "error": "No hay ninguna canción reproduciéndose actualmente"
                }
        elif response.status_code == 204:
            return {
                "success": False,
                "error": "No hay ninguna canción reproduciéndose actualmente"
            }
        elif response.status_code == 403:
            return {
                "success": False,
                "error": "Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "No hay dispositivos activos."
            }
        else:
            return {
                "success": False,
                "error": f"Error obteniendo canción actual: {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error de conexión: {str(e)}"
        }

def search_and_play(query):
    """Buscar una canción y reproducirla automáticamente"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Paso 1: Buscar la canción
        search_params = {
            'q': query,
            'type': 'track',
            'limit': 1,  # Solo necesitamos el primer resultado
            'market': 'ES'
        }
        
        search_response = requests.get(
            'https://api.spotify.com/v1/search',
            headers=headers,
            params=search_params,
            timeout=10
        )
        
        if search_response.status_code != 200:
            return {"success": False, "error": f"Error en búsqueda: HTTP {search_response.status_code}"}
        
        search_data = search_response.json()
        tracks = search_data.get('tracks', {}).get('items', [])
        
        if not tracks:
            return {"success": False, "error": f"No se encontraron resultados para: '{query}'"}
        
        # Obtener información de la primera canción encontrada
        track = tracks[0]
        track_uri = track['uri']
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        
        # Paso 2: Obtener dispositivo activo
        device_id = get_active_device()
        if not device_id:
            return {
                "success": False, 
                "error": "No hay dispositivo activo",
                "found_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }
        
        # Paso 3: Reproducir la canción
        play_data = {
            'uris': [track_uri],
            'position_ms': 0
        }
        
        play_response = requests.put(
            f'https://api.spotify.com/v1/me/player/play?device_id={device_id}',
            headers=headers,
            json=play_data,
            timeout=10
        )
        
        if play_response.status_code == 204:
            return {
                "success": True,
                "action": "search_and_play",
                "track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name,
                    "uri": track_uri
                },
                "device_id": device_id
            }
        elif play_response.status_code == 403:
            return {
                "success": False, 
                "error": "Token expirado o permisos insuficientes",
                "found_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }
        elif play_response.status_code == 404:
            return {
                "success": False, 
                "error": "Dispositivo no encontrado",
                "found_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }
        else:
            return {
                "success": False, 
                "error": f"Error reproduciendo: HTTP {play_response.status_code}",
                "found_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }

    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

def create_personal_release_radar(weeks_back=4, include_features=True, playlist_name=None):
    """Crear playlist con lanzamientos recientes de artistas que sigues y te gustan"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        from datetime import datetime, timedelta
        import time
        
        current_date = datetime.now()
        cutoff_date = current_date - timedelta(weeks=weeks_back)
        recent_tracks = []
        artists_processed = set()
        
        # Paso 1: Obtener artistas que sigues
        following_response = requests.get(
            'https://api.spotify.com/v1/me/following?type=artist&limit=30',
            headers=headers,
            timeout=10
        )
        
        followed_artists = []
        if following_response.status_code == 200:
            followed_artists = following_response.json().get('artists', {}).get('items', [])
        
        # Paso 2: Obtener tus top artistas
        top_artists_response = requests.get(
            'https://api.spotify.com/v1/me/top/artists?limit=20&time_range=medium_term',
            headers=headers,
            timeout=10
        )
        
        top_artists = []
        if top_artists_response.status_code == 200:
            top_artists = top_artists_response.json().get('items', [])
        
        # Combinar artistas (evitar duplicados)
        all_artists = []
        for artist in followed_artists + top_artists:
            if artist['id'] not in artists_processed:
                all_artists.append(artist)
                artists_processed.add(artist['id'])
        
        # Paso 3: Buscar lanzamientos recientes de cada artista
        for i, artist in enumerate(all_artists[:25]):  # Limitar a 25 artistas para no saturar
            try:
                # Obtener álbumes recientes del artista
                albums_response = requests.get(
                    f'https://api.spotify.com/v1/artists/{artist["id"]}/albums?limit=10&album_type=album,single&market=US',
                    headers=headers,
                    timeout=10
                )
                
                if albums_response.status_code == 200:
                    albums = albums_response.json().get('items', [])
                    
                    for album in albums:
                        # Verificar fecha de lanzamiento
                        release_date_str = album.get('release_date', '')
                        if not release_date_str:
                            continue
                        
                        try:
                            # Manejar diferentes formatos de fecha
                            if len(release_date_str) == 4:  # Solo año
                                release_date = datetime.strptime(f"{release_date_str}-01-01", '%Y-%m-%d')
                            elif len(release_date_str) == 7:  # Año-mes
                                release_date = datetime.strptime(f"{release_date_str}-01", '%Y-%m-%d')
                            else:  # Fecha completa
                                release_date = datetime.strptime(release_date_str, '%Y-%m-%d')
                            
                            # Verificar si es reciente
                            if release_date >= cutoff_date:
                                # Obtener tracks del álbum/single
                                album_tracks_response = requests.get(
                                    f'https://api.spotify.com/v1/albums/{album["id"]}/tracks?limit=5',
                                    headers=headers,
                                    timeout=10
                                )
                                
                                if album_tracks_response.status_code == 200:
                                    album_tracks = album_tracks_response.json().get('items', [])
                                    
                                    for track in album_tracks[:3]:  # Max 3 tracks por álbum
                                        track['_release_date'] = release_date_str
                                        track['_album_name'] = album['name']
                                        track['_artist_name'] = artist['name']
                                        recent_tracks.append(track)
                        
                        except ValueError:
                            # Si no se puede parsear la fecha, saltar
                            continue
                
                # Pausa pequeña para no saturar la API
                if i % 5 == 0:
                    time.sleep(0.1)
                    
            except Exception as e:
                # Continuar con el siguiente artista si hay error
                continue
        
        # Paso 4: Si include_features, buscar colaboraciones recientes
        if include_features and len(recent_tracks) < 20:  # Solo si necesitamos más tracks
            for artist in all_artists[:10]:  # Limitar búsqueda de features
                try:
                    features_response = requests.get(
                        f'https://api.spotify.com/v1/search?q=artist:"{artist["name"]}"&type=track&limit=8&market=US',
                        headers=headers,
                        timeout=10
                    )
                    
                    if features_response.status_code == 200:
                        feature_tracks = features_response.json().get('tracks', {}).get('items', [])
                        
                        for track in feature_tracks[:3]:  # Max 3 por artista
                            # Verificar que no sea del artista principal (que sea feature)
                            main_artist = track['artists'][0]['name'].lower()
                            if artist['name'].lower() != main_artist:
                                track['_is_feature'] = True
                                track['_artist_name'] = artist['name']
                                recent_tracks.append(track)
                        
                        time.sleep(0.1)
                        
                except Exception:
                    continue
        
        if not recent_tracks:
            return {
                "success": False, 
                "error": f"No se encontraron lanzamientos recientes en las últimas {weeks_back} semanas"
            }
        
        # Paso 5: Eliminar duplicados y ordenar por fecha
        unique_tracks = []
        seen_ids = set()
        
        for track in recent_tracks:
            if track and track.get('id') and track['id'] not in seen_ids:
                unique_tracks.append(track)
                seen_ids.add(track['id'])
        
        # Ordenar por fecha de lanzamiento (más recientes primero)
        unique_tracks.sort(key=lambda x: x.get('_release_date', ''), reverse=True)
        
        # Limitar a máximo 30 tracks
        unique_tracks = unique_tracks[:30]
        
        # Paso 6: Crear playlist
        if not playlist_name:
            playlist_name = f"Personal Release Radar - {current_date.strftime('%b %Y')}"
        
        # Obtener información del usuario
        user_response = requests.get('https://api.spotify.com/v1/me', headers=headers, timeout=10)
        if user_response.status_code != 200:
            return {"success": False, "error": "No se pudo obtener información del usuario"}
        
        user_id = user_response.json()['id']
        
        # Crear playlist
        playlist_data = {
            "name": playlist_name,
            "description": f"Fresh releases from your followed and top artists (last {weeks_back} weeks)",
            "public": False
        }
        
        playlist_response = requests.post(
            f'https://api.spotify.com/v1/users/{user_id}/playlists',
            headers=headers,
            json=playlist_data,
            timeout=10
        )
        
        if playlist_response.status_code != 201:
            return {"success": False, "error": f"Error creando playlist: HTTP {playlist_response.status_code}"}
        
        playlist = playlist_response.json()
        playlist_id = playlist['id']
        
        # Paso 7: Agregar tracks a la playlist
        track_uris = [track['uri'] for track in unique_tracks if track.get('uri')]
        
        if track_uris:
            add_tracks_response = requests.post(
                f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
                headers=headers,
                json={"uris": track_uris},
                timeout=10
            )
            
            if add_tracks_response.status_code != 201:
                return {"success": False, "error": f"Error agregando tracks: HTTP {add_tracks_response.status_code}"}
        
        # Contar estadísticas
        artists_count = len(set(track.get('_artist_name', 'Unknown') for track in unique_tracks))
        features_count = len([track for track in unique_tracks if track.get('_is_feature')])
        
        return {
            "success": True,
            "action": "create_personal_release_radar",
            "playlist": {
                "name": playlist_name,
                "id": playlist_id,
                "url": playlist['external_urls']['spotify'],
                "tracks_count": len(track_uris),
                "period_weeks": weeks_back,
                "artists_count": artists_count,
                "features_count": features_count if include_features else 0
            },
            "stats": {
                "total_tracks_found": len(unique_tracks),
                "from_followed_artists": len([t for t in unique_tracks if not t.get('_is_feature')]),
                "features": features_count if include_features else 0
            }
        }
        
    except Exception as e:
        return {"success": False, "error": f"Error creando Release Radar Personal: {str(e)}"}

def play_top_track(time_range="medium_term", limit=20):
    """Reproducir una canción aleatoria de tus top tracks"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        import random
        
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Paso 1: Obtener top tracks
        params = {
            'time_range': time_range,
            'limit': limit,
            'offset': 0
        }
        
        top_tracks_response = requests.get(
            'https://api.spotify.com/v1/me/top/tracks',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if top_tracks_response.status_code != 200:
            return {
                "success": False, 
                "error": f"Error obteniendo top tracks: HTTP {top_tracks_response.status_code}"
            }
        
        top_tracks_data = top_tracks_response.json()
        tracks = top_tracks_data.get('items', [])
        
        if not tracks:
            return {
                "success": False, 
                "error": f"No se encontraron top tracks para el período {time_range}"
            }
        
        # Paso 2: Seleccionar track aleatorio
        random_track = random.choice(tracks)
        track_uri = random_track['uri']
        track_name = random_track['name']
        artists = ', '.join([artist['name'] for artist in random_track['artists']])
        album_name = random_track['album']['name']
        
        # Paso 3: Verificar dispositivo activo
        device_id = get_active_device()
        if not device_id:
            return {
                "success": False,
                "error": "No hay dispositivo activo",
                "selected_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name,
                    "time_range": time_range
                }
            }
        
        # Paso 4: Reproducir la canción
        play_data = {
            'uris': [track_uri],
            'position_ms': 0
        }
        
        play_response = requests.put(
            f'https://api.spotify.com/v1/me/player/play?device_id={device_id}',
            headers=headers,
            json=play_data,
            timeout=10
        )
        
        if play_response.status_code == 204:
            return {
                "success": True,
                "action": "play_top_track",
                "track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name,
                    "uri": track_uri
                },
                "stats": {
                    "total_top_tracks": len(tracks),
                    "time_range": time_range,
                    "selected_from": f"top {len(tracks)} tracks"
                },
                "device_id": device_id
            }
        elif play_response.status_code == 403:
            return {
                "success": False,
                "error": "Token expirado o permisos insuficientes",
                "selected_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }
        elif play_response.status_code == 404:
            return {
                "success": False,
                "error": "Dispositivo no encontrado",
                "selected_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }
        else:
            return {
                "success": False,
                "error": f"Error reproduciendo: HTTP {play_response.status_code}",
                "selected_track": {
                    "name": track_name,
                    "artist": artists,
                    "album": album_name
                }
            }
            
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

def get_top_tracks(time_range="medium_term", limit=20):
    """Obtener lista de tus top tracks sin reproducir"""
    if not ACCESS_TOKEN:
        return {"success": False, "error": "ACCESS_TOKEN no configurado en .env"}
    
    try:
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Parámetros para la API
        params = {
            'time_range': time_range,
            'limit': limit,
            'offset': 0
        }
        
        response = requests.get(
            'https://api.spotify.com/v1/me/top/tracks',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('items', [])
            
            if not tracks:
                return {
                    "success": False, 
                    "error": f"No se encontraron top tracks para el período {time_range}"
                }
            
            # Formatear la respuesta con información de los tracks
            formatted_tracks = []
            for i, track in enumerate(tracks, 1):
                artists = ', '.join([artist['name'] for artist in track['artists']])
                formatted_tracks.append({
                    "position": i,
                    "name": track['name'],
                    "artist": artists,
                    "album": track['album']['name'],
                    "popularity": track.get('popularity', 0),
                    "uri": track['uri']
                })
            
            return {
                "success": True,
                "time_range": time_range,
                "total_tracks": len(formatted_tracks),
                "tracks": formatted_tracks
            }
            
        elif response.status_code == 403:
            return {
                "success": False,
                "error": "Token expirado o no tiene permisos para 'user-top-read'. Ejecuta spotify_auth.py de nuevo con todos los scopes."
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Token inválido. Ejecuta spotify_auth.py de nuevo."
            }
        elif response.status_code == 429:
            return {
                "success": False,
                "error": "Demasiadas requests. Espera un momento e intenta de nuevo."
            }
        else:
            return {
                "success": False,
                "error": f"Error obteniendo top tracks: HTTP {response.status_code}"
            }
            
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

# MCP Server Implementation
server = Server("spotify-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="next_track",
            description="Skip to next track on active Spotify device",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="previous_track",
            description="Go to previous track on active Spotify device",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="pause_track",
            description="Pause playback on active Spotify device",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="resume_track",
            description="Resume/play playback on active Spotify device",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="current_track",
            description="Get information about the currently playing track on Spotify",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="search_and_play",
            description="Search for a song on Spotify and play it immediately",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for the song (artist, song name, album, etc.)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_top_tracks",
            description="Get your top tracks from Spotify without playing them",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_range": {
                        "type": "string",
                        "description": "Time period for top tracks",
                        "enum": ["short_term", "medium_term", "long_term"],
                        "default": "medium_term"
                    },
                    "limit": {
                        "type": "integer", 
                        "description": "Number of top tracks to get (1-50)",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 20
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="play_top_track",
            description="Play a random song from your top tracks on Spotify",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_range": {
                        "type": "string",
                        "description": "Time period for top tracks",
                        "enum": ["short_term", "medium_term", "long_term"],
                        "default": "medium_term"
                    },
                    "limit": {
                        "type": "integer", 
                        "description": "Number of top tracks to choose from (1-50)",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 20
                    }
                },
                "required": []
            }
        ),

    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    
    if name == "next_track":
        result = next_track()
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "previous_track":
        result = previous_track()
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "pause_track":
        result = pause_track()
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "resume_track":
        result = resume_track()
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "current_track":
        result = current_track()
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "search_and_play":
        query = arguments.get("query", "")
        if not query:
            error_result = {"success": False, "error": "Se requiere un término de búsqueda"}
            return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]
        result = search_and_play(query)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "get_top_tracks":
        time_range = arguments.get("time_range", "medium_term")
        limit = arguments.get("limit", 20)
        
        # Validar parámetros
        if time_range not in ["short_term", "medium_term", "long_term"]:
            error_result = {"success": False, "error": "time_range debe ser: short_term, medium_term, o long_term"}
            return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]
        
        if not (1 <= limit <= 50):
            error_result = {"success": False, "error": "limit debe estar entre 1 y 50"}
            return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]
            
        result = get_top_tracks(time_range, limit)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    elif name == "play_top_track":
        time_range = arguments.get("time_range", "medium_term")
        limit = arguments.get("limit", 20)
        
        # Validar time_range
        if time_range not in ["short_term", "medium_term", "long_term"]:
            error_result = {"success": False, "error": "time_range debe ser: short_term, medium_term, o long_term"}
            return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]
        
        # Validar limit
        if not (1 <= limit <= 50):
            error_result = {"success": False, "error": "limit debe estar entre 1 y 50"}
            return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]
            
        result = play_top_track(time_range, limit)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    else:
        error_result = {"success": False, "error": f"Herramienta desconocida: {name}"}
        return [TextContent(type="text", text=json.dumps(error_result, ensure_ascii=False, indent=2))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    # Verificar que el token esté configurado
    if not ACCESS_TOKEN:
        print(" ERROR: Debes agregar SPOTIFY_ACCESS_TOKEN en el archivo .env")
        print("1. Ejecuta spotify_auth.py para obtener el token")
        print("2. Agrega SPOTIFY_ACCESS_TOKEN=tu_token en .env")
        exit(1)
    
    # Modo test directo
    # import sys
    # if len(sys.argv) == 1:
    #     print("Probando next_track...")
    #     result = next_track()
    #     print(result)
    else:
        # Modo MCP server (sin prints que interfieran con JSON)
        import asyncio
        asyncio.run(main())
