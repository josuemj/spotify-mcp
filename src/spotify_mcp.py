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
        
        if response.status_code == 200:
            return f" Saltó a la siguiente canción en dispositivo {device_id}"
        elif response.status_code == 403:
            return "Error: Token expirado o permisos insuficientes. Ejecuta spotify_auth.py de nuevo."
        elif response.status_code == 404:
            return "Error: No hay dispositivos activos o no se encontró el dispositivo."
        else:
            return f"Error saltando canción: {response.status_code}"
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
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "next_track":
        result = next_track()
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
