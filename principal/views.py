from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User # Importamos User por si acaso

from .models import CanalTransmision, Cliente

# ============================
# UTIL
# ============================
def build_hls_url(filename: str) -> str:
    """Construye la URL final del stream HLS"""
    base = settings.HLS_BASE_URL.rstrip("/")
    program = settings.HLS_PROGRAM_PATH.strip("/")
    return f"{base}/{program}/{filename}"

# ============================
# HOME / CANAL OFICIAL
# ============================
def home_view(request):
    stream_data = {
        'name': "Kaircam Oficial",
        'hls_url': build_hls_url("publicidad.m3u8"),
        'en_vivo': True,
    }

    return render(request, 'principal/home.html', {
        'stream': stream_data,
        'es_home': True,
        'cliente': None
    })

# ============================
# BÚSQUEDA DE CANALES
# ============================
def search_view(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('home')

    # Buscamos si existe el canal
    canal = CanalTransmision.objects.filter(usuario__username__iexact=query).first()

    if canal:
        # Si existe, vamos a su perfil
        return redirect('usuario_stream', username=canal.usuario.username)
    else:
        # Si NO existe, mandamos alerta y quedamos en home
        messages.error(request, f"❌ El usuario '{query}' no fue encontrado.")
        return redirect('home')

# ============================
# CANAL DE USUARIO (PÚBLICO)
# ============================
def usuario_stream_view(request, username):
    # 1. Intentamos obtener el canal. Usamos filter().first() para no romper con error 404
    canal = CanalTransmision.objects.filter(usuario__username=username).first()
    
    # === AQUÍ ESTÁ EL CAMBIO IMPORTANTE ===
    if not canal:
        # Si el usuario pone una URL falsa, lo devolvemos al home con un cartel rojo
        messages.error(request, f"⚠️ El canal de '{username}' no existe o no está disponible.")
        return redirect('home')
    # ======================================

    # 2. Intentar obtener los datos sociales del Cliente
    cliente = Cliente.objects.filter(user=canal.usuario).first()

    # 3. Preparar datos del stream
    hls_final = canal.url_hls if hasattr(canal, 'url_hls') and canal.url_hls else build_hls_url(f"{canal.usuario.username}.m3u8")

    stream_data = {
        'name': f"Canal de {canal.usuario.username}",
        'hls_url': hls_final,
        'en_vivo': canal.en_vivo,
    }

    return render(request, 'principal/home.html', {
        'stream': stream_data,
        'es_home': False,
        'streamer_name': canal.usuario.username,
        'cliente': cliente,
    })