from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings

from .models import CanalTransmision


# ============================
# UTIL
# ============================
def build_hls_url(filename: str) -> str:
    """
    Construye la URL final del stream HLS
    Ej:
    https://dominio/hls/program/usuario.m3u8
    """
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
        'en_vivo': True,  # más adelante puede venir de DB
    }

    return render(request, 'principal/home.html', {
        'stream': stream_data,
        'es_home': True,
    })


# ============================
# BÚSQUEDA DE CANALES
# ============================
def search_view(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('home')

    canal = CanalTransmision.objects.filter(
        usuario__username__iexact=query
    ).first()

    if canal:
        return redirect('usuario_stream', username=canal.usuario.username)

    messages.warning(
        request,
        f"El canal '{query}' no fue encontrado. Revisa el nombre e intenta de nuevo."
    )
    return redirect('home')


# ============================
# CANAL DE USUARIO (PÚBLICO)
# ============================
def usuario_stream_view(request, username):
    canal = get_object_or_404(
        CanalTransmision,
        usuario__username=username
    )

    stream_data = {
        'name': f"Canal de {canal.usuario.username}",
        'hls_url': build_hls_url(f"{canal.usuario.username}.m3u8"),
        'en_vivo': canal.en_vivo,
    }

    return render(request, 'principal/home.html', {
        'stream': stream_data,
        'es_home': False,
        'streamer_name': canal.usuario.username,
    })
