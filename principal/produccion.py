# ============================================================
# GUÍA COMPLETA PARA FRONTEND DE STREAMING (CON MANYCAM)
# ============================================================
# Objetivo: Documentar paso a paso cómo funciona el frontend,
# qué se modifica ahora y qué se deja listo para producción.
# ============================================================

# 1) MODELO STREAM (models.py)
# ----------------------------
# El modelo ya está definido. Sus campos son:
# - name: nombre de la transmisión (ej. "Cliente A")
# - stream_key: clave única que usa ManyCam para enviar RTMP
# - hls_url: URL pública al archivo .m3u8 generado por el servidor
# - is_active: indica si el stream está en vivo
# - created_at: fecha de creación
#
# IMPORTANTE: el frontend NO crea ni administra estos campos,
# solo los consume. El panel de control o el admin de Django
# son los que rellenan estos valores.

# 2) MANYCAM (TELÉFONO COMO ENCODER)
# ----------------------------------
# - En ManyCam configurás la salida RTMP:
#   Servidor: rtmp://stream.tudominio.com/live
#   Stream key: clienteA123 (ejemplo)
# - El servidor de streaming recibe ese RTMP y genera un HLS (.m3u8):
#   https://stream.tudominio.com/hls/clienteA/index.m3u8
# - Esa URL se guarda en el campo hls_url del modelo Stream.

# 3) CREACIÓN DE STREAMS (ADMIN O PANEL)
# --------------------------------------
# - Desde el admin de Django (/admin/) podés crear un Stream:
#   name = "Cliente A"
#   stream_key = "clienteA123"
#   hls_url = "https://stream.tudominio.com/hls/clienteA/index.m3u8"
#   is_active = True
# - También se puede crear desde el panel de control (otro proyecto).
# - El frontend solo necesita que exista un Stream activo en la base.

# 4) VISTAS (views.py)
# --------------------
# def home(request):
#     stream = Stream.objects.filter(is_active=True).first()
#     return render(request, "principal/home.html", {"stream": stream})
#
# def stream_view(request, stream_id):
#     stream = get_object_or_404(Stream, id=stream_id)
#     return render(request, "principal/stream.html", {"stream": stream})
#
# - home: muestra el primer stream activo.
# - stream_view: muestra un stream específico por ID (cada cliente con su página).

# 5) URLS (urls.py)
# -----------------
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('stream/<int:stream_id>/', views.stream_view, name='stream_view'),
# ]
#
# Ejemplos:
# - https://www.tudominio.com/ → muestra el activo
# - https://www.tudominio.com/stream/1/ → muestra el stream con ID=1

# 6) TEMPLATES (home.html / stream.html)
# --------------------------------------
# {% if stream %}
#   <video id="mainStream" controls autoplay playsinline>
#     <source src="{{ stream.hls_url }}" type="application/x-mpegURL">
#   </video>
# {% else %}
#   <p>No hay transmisiones en vivo</p>
# {% endif %}
#
# - El campo hls_url se usa directamente en el <source>.
# - No se necesita lógica extra: si el panel/admin cargó el stream,
#   el frontend lo reproduce automáticamente.

# 7) BOTÓN DE LOGIN (base.html)
# -----------------------------
# <div class="navbar-actions">
#   <a href="https://www.google.com" target="_blank" rel="noopener" class="btn-secondary">Iniciar Sesión</a>
# </div>
#
# - Quitar el botón de "Registrarse".
# - Dejar solo "Iniciar Sesión".
# - target="_blank" abre en nueva pestaña.
# - Más adelante cambiar href por la URL real del panel.

# 8) SETTINGS DE PRODUCCIÓN (settings.py)
# ---------------------------------------
# - DEBUG = False
# - ALLOWED_HOSTS = ["tudominio.com", "www.tudominio.com", "IP"]
# - Configurar STATIC_ROOT y correr: python manage.py collectstatic
# - Configurar Nginx con SSL (Let's Encrypt) y redirección http→https.

# 9) FLUJO COMPLETO
# -----------------
# ManyCam (teléfono) → RTMP (con stream_key) → Servidor de streaming (Nginx RTMP/MediaMTX) → genera HLS (.m3u8) →
# Panel/Admin guarda hls_url en Stream → Frontend muestra {{ stream.hls_url }} en <video>

# 10) RESUMEN
# -----------
# - El frontend NO crea streams, solo los consume.
# - Los campos se rellenan en el panel o admin.
# - Con lo que ya hicimos, el consumo es automático:
#   si hay un Stream activo con hls_url válido, se muestra en la web.
# ============================================================
# ============================================================
# GUÍA COMPLETA PARA FRONTEND DE STREAMING (CON MANYCAM) - PARTE FINAL
# ============================================================

# 11) AUTOMATIZACIÓN DEL CONSUMO DE STREAMS
# -----------------------------------------
# - El frontend NO necesita lógica adicional para "activar" un stream.
# - Con las vistas y templates que ya hicimos, el consumo es automático:
#   * Si existe un Stream en la base con is_active=True y hls_url válido,
#     se mostrará en el home.html.
#   * Si accedés a /stream/<id>/, se mostrará el Stream con ese ID.
# - No hay que programar nada extra en este proyecto para que funcione.

# 12) EJEMPLO DE CREACIÓN DE STREAM EN ADMIN DJANGO
# -------------------------------------------------
# - Entrar a /admin/ con tu usuario superuser.
# - Crear un nuevo Stream:
#   name: "Cliente A"
#   stream_key: "clienteA123"  # clave que se usa en ManyCam
#   hls_url: "https://stream.tudominio.com/hls/clienteA/index.m3u8"
#   is_active: True
# - Guardar. Automáticamente el frontend mostrará ese stream.

# 13) EJEMPLO DE CONFIGURACIÓN EN MANYCAM (TELÉFONO)
# --------------------------------------------------
# - Abrir ManyCam en el teléfono.
# - Ir a "Broadcast" o "Stream".
# - Configurar salida RTMP:
#   Servidor: rtmp://stream.tudominio.com/live
#   Stream key: clienteA123
# - Al iniciar transmisión, el servidor genera el HLS (.m3u8).
# - Esa URL debe estar guardada en hls_url del modelo Stream.

# 14) FLUJO COMPLETO (RESUMEN)
# ----------------------------
# ManyCam (teléfono) → RTMP (con stream_key) → Servidor de streaming (Nginx RTMP/MediaMTX) → genera HLS (.m3u8) →
# Panel/Admin guarda hls_url en Stream → Frontend muestra {{ stream.hls_url }} en <video>

# 15) PUNTOS ÚNICOS DE CAMBIO EN PRODUCCIÓN
# -----------------------------------------
# - base.html → cambiar href del botón "Iniciar Sesión" al panel real.
# - settings.py → actualizar ALLOWED_HOSTS con dominio final.
# - Stream.hls_url → se actualiza desde el panel/admin con la URL real del .m3u8.
# - Nginx → ajustar server_name y certificados SSL cuando el dominio esté activo.

# 16) VALIDACIÓN FINAL
# --------------------
# - Crear un Stream en admin con hls_url válido y is_active=True.
# - Abrir https://www.tudominio.com/ → debe mostrar el stream activo.
# - Abrir https://www.tudominio.com/stream/<id>/ → debe mostrar el stream específico.
# - Probar el botón "Iniciar Sesión" → debe abrir nueva pestaña con la URL configurada.
# - Verificar reproducción en Chrome, Firefox, Safari/iOS y Android.

# ============================================================
# CON ESTO EL FRONTEND QUEDA LISTO PARA PRODUCCIÓN
# ============================================================
# - No hay que programar nada más para consumir streams.
# - El panel/admin se encarga de crear y activar streams.
# - El frontend automáticamente los muestra en home o por ID.
# ============================================================
# ============================================================
# GUÍA COMPLETA PARA FRONTEND DE STREAMING (CON MANYCAM) - EXTENSIÓN
# ============================================================

# 17) DIFERENCIA ENTRE INGESTA Y CONSUMO
# --------------------------------------
# - INGESTA: el encoder (ManyCam en el teléfono) envía RTMP al servidor.
#   Ejemplo: rtmp://stream.tudominio.com/live/clienteA123
# - CONSUMO: el navegador recibe HLS (.m3u8) y lo reproduce en <video>.
#   Ejemplo: https://stream.tudominio.com/hls/clienteA/index.m3u8
# - El frontend solo participa en la parte de consumo.

# 18) AUTOMATIZACIÓN DEL FRONTEND
# -------------------------------
# - No se necesita ninguna view para crear streams en este proyecto.
# - El frontend ya está listo para consumir automáticamente:
#   * home.html → muestra el primer stream activo.
#   * stream.html → muestra el stream específico por ID.
# - Cuando el panel/admin actualiza la base con un hls_url válido y is_active=True,
#   el frontend lo mostrará sin cambios de código.

# 19) EJEMPLO DE USO REAL
# -----------------------
# Paso 1: Configurar ManyCam en el teléfono
#   Servidor: rtmp://stream.tudominio.com/live
#   Stream key: clienteA123
#
# Paso 2: El servidor genera HLS
#   URL: https://stream.tudominio.com/hls/clienteA/index.m3u8
#
# Paso 3: Guardar en la base (admin/panel)
#   name = "Cliente A"
#   stream_key = "clienteA123"
#   hls_url = "https://stream.tudominio.com/hls/clienteA/index.m3u8"
#   is_active = True
#
# Paso 4: Frontend
#   - Home: muestra automáticamente el stream activo.
#   - /stream/1/: muestra el stream con ID=1.

# 20) VALIDACIÓN EN PRODUCCIÓN
# ----------------------------
# - Verificar que el .m3u8 se carga en navegador (Chrome, Safari, Firefox).
# - Probar en iOS/Android con playsinline y muted si autoplay falla.
# - Revisar que el botón "Iniciar Sesión" abre nueva pestaña al panel.
# - Confirmar que ALLOWED_HOSTS y SSL están configurados en Django/Nginx.

# 21) MANTENIMIENTO FUTURO
# ------------------------
# - Solo se actualizan:
#   * base.html → href del botón login.
#   * settings.py → dominios finales en ALLOWED_HOSTS.
#   * Stream.hls_url → actualizado por panel/admin.
# - No se requieren cambios en views ni templates para consumir streams.

# ============================================================
# CONCLUSIÓN
# ============================================================
# - El frontend está completo: consume automáticamente cualquier stream activo.
# - ManyCam envía RTMP → servidor genera HLS → panel/admin guarda hls_url.
# - El frontend muestra el stream sin necesidad de lógica adicional.
# ============================================================
