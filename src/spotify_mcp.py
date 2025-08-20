import os
import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

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
        return "Error: ACCESS_TOKEN no configurado en .env"
    
    try:
        device_id = get_active_device()
        if not device_id:
            return "No hay dispositivo activo encontrado. Asegúrate de que Spotify esté reproduciéndose."
        
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
        
        if response.status_code == 200:  # 204 es el código correcto
            return f"Saltó a la siguiente canción en dispositivo {device_id}"
        elif response.status_code == 403:
            return "Error: Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
        elif response.status_code == 404:
            return "Error: No hay dispositivos activos o no se encontró el dispositivo."
        else:
            return f"Error saltando canción: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def previous_track():
    """Ir a la canción anterior en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return "Error: ACCESS_TOKEN no configurado en .env"
    
    try:
        device_id = get_active_device()
        if not device_id:
            return "No hay dispositivo activo encontrado. Asegúrate de que Spotify esté reproduciéndose."
        
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
            return f"Fue a la canción anterior en dispositivo {device_id}"
        elif response.status_code == 403:
            return "Error: Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
        elif response.status_code == 404:
            return "Error: No hay dispositivos activos o no se encontró el dispositivo."
        else:
            return f"Error yendo a canción anterior: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def pause_track():
    """Pausar la reproducción en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return "Error: ACCESS_TOKEN no configurado en .env"
    
    try:
        device_id = get_active_device()
        if not device_id:
            return "No hay dispositivo activo encontrado. Asegúrate de que Spotify esté reproduciéndose."
        
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
            return f"Pausó la reproducción en dispositivo {device_id}"
        elif response.status_code == 403:
            return "Error: Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
        elif response.status_code == 404:
            return "Error: No hay dispositivos activos o no se encontró el dispositivo."
        else:
            return f"Error pausando reproducción: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def resume_track():
    """Reanudar la reproducción en el dispositivo activo"""
    if not ACCESS_TOKEN:
        return "Error: ACCESS_TOKEN no configurado en .env"
    
    try:
        device_id = get_active_device()
        if not device_id:
            return "No hay dispositivo activo encontrado. Asegúrate de que Spotify esté reproduciéndose."
        
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
            return f"Reanudó la reproducción en dispositivo {device_id}"
        elif response.status_code == 403:
            return "Error: Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
        elif response.status_code == 404:
            return "Error: No hay dispositivos activos o no se encontró el dispositivo."
        else:
            return f"Error reanudando reproducción: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def current_track():
    """Obtener información de la canción que se está reproduciendo actualmente"""
    if not ACCESS_TOKEN:
        return "Error: ACCESS_TOKEN no configurado en .env"
    
    try:
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Hacer request a currently-playing
        response = requests.get(
            'https://api.spotify.com/v1/me/player/currently-playing', 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data and 'item' in data:
                track = data['item']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                track_name = track['name']
                album_name = track['album']['name']
                is_playing = data.get('is_playing', False)
                duration_ms = track.get('duration_ms', 0)

                return {
                    "track": track_name,
                    "artist": artists,
                    "album": album_name,
                    "status": "Reproduciendo" if is_playing else "Pausado",
                    "duration" : f"{duration_ms // 60000}:{(duration_ms % 60000) // 1000:02d}"
                }
            else:
                return "No hay ninguna canción reproduciéndose actualmente"
                
        elif response.status_code == 204:
            return "No hay ninguna canción reproduciéndose actualmente"
        elif response.status_code == 403:
            return "Error: Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
        elif response.status_code == 404:
            return "Error: No hay dispositivos activos."
        else:
            return f"Error obteniendo canción actual: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

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
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "next_track":
        result = next_track()
        return [TextContent(type="text", text=result)]
    elif name == "previous_track":
        result = previous_track()
        return [TextContent(type="text", text=result)]
    elif name == "pause_track":
        result = pause_track()
        return [TextContent(type="text", text=result)]
    elif name == "resume_track":
        result = resume_track()
        return [TextContent(type="text", text=result)]
    elif name == "current_track":
        result = current_track()
        return [TextContent(type="text", text=result)]
    else:
        raise ValueError(f"Unknown tool: {name}")

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
