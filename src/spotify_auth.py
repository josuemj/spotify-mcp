import os
import requests
import base64
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'https://github.com/josuemj/mcp-llm-client'
SCOPE = 'user-read-playback-state user-modify-playback-state'

def get_authorization_url():
    """Genera la URL de autorización de Spotify"""
    auth_params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'show_dialog': 'true'
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(auth_params)}"
    return auth_url

def get_access_token(auth_code):
    """Intercambia el código de autorización por un access token"""
    # Crear las credenciales en base64
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    credentials_b64 = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {credentials_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data
    else:
        print(f"Error obteniendo token: {response.status_code}")
        print(response.text)
        return None

def authorize_spotify():
    """Flujo completo de autorización"""
    print("=== Autorización de Spotify ===")
    
    # Generar y mostrar URL de autorización
    auth_url = get_authorization_url()
    print(f"1. Abre este link para autorizar:")
    print(f"{auth_url}")
    print()
    
    # Abrir navegador automáticamente
    try:
        webbrowser.open(auth_url)
        print("✓Navegador abierto automáticamente")
    except:
        print("!No se pudo abrir el navegador automáticamente")
    
    print()
    print("2. Después de autorizar, serás redirigido a una URL.")
    print("3. Copia esa URL completa y pégala aquí:")
    
    # Pedir URL de redirección
    redirect_url = input("URL de redirección: ").strip()
    
    # Extraer el código de la URL
    try:
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        auth_code = query_params.get('code', [None])[0]
        
        if not auth_code:
            print(" No se encontró el código en la URL")
            return None
            
        print(f"✓ Código extraído: {auth_code[:20]}...")
        
        # Obtener access token
        print("Obteniendo access token...")
        token_data = get_access_token(auth_code)
        
        if token_data:
            print(" Access token obtenido exitosamente!")
            print(f"Token expira en: {token_data.get('expires_in', 'N/A')} segundos")
            
            # Guardar token en .env
            access_token = token_data['access_token']
            
            # Leer el archivo .env actual
            env_path = '.env'
            env_lines = []
            
            # Leer líneas existentes si el archivo existe
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    env_lines = f.readlines()
            
            # Buscar si ya existe SPOTIFY_ACCESS_TOKEN y actualizarlo o agregarlo
            token_line = f"\nSPOTIFY_ACCESS_TOKEN={access_token}\n"
            updated = False
            
            for i, line in enumerate(env_lines):
                if line.startswith('SPOTIFY_ACCESS_TOKEN='):
                    env_lines[i] = token_line
                    updated = True
                    break
            
            # Si no existía, agregarlo al final
            if not updated:
                env_lines.append(token_line)
            
            # Escribir el archivo .env actualizado
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(env_lines)
            
            print("✅ ACCESS_TOKEN guardado en .env")
            
            return token_data
        else:
            print(" Error obteniendo access token")
            return None
            
    except Exception as e:
        print(f" Error procesando URL: {e}")
        return None

if __name__ == "__main__":
    token_data = authorize_spotify()
    if token_data:
        print(f"Access Token: {token_data['access_token'][:50]}...")
