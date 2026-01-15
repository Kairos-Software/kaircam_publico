from django.db import models
from django.contrib.auth.models import User

class CanalTransmision(models.Model):
    # Usamos DO_NOTHING para que si borras algo en el público no afecte al panel
    usuario = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="canal_transmision_pub")
    en_vivo = models.BooleanField(default=False)
    
    # Si añades url_hls en el panel, añádelo aquí también:
    url_hls = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False          # Django no creará ni modificará esta tabla
        db_table = 'core_canaltransmision'  # Mismo nombre que en el Panel

    def __str__(self):
        return f"Canal de {self.usuario.username}"


class Cliente(models.Model):
    """
    Modelo espejo (managed=False) para leer los datos sociales creados en el Panel.
    Apunta a la tabla 'core_cliente'.
    """
    # En el modelo original del panel, el campo es: user = OneToOneField(...)
    # En la base de datos la columna se llama 'user_id'.
    user = models.OneToOneField(
        User, 
        on_delete=models.DO_NOTHING, 
        related_name="cliente_publico",
        db_column='user_id' 
    )
    
    # Datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    # Redes Sociales (Mismos nombres que en core/models.py)
    bio = models.TextField(blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    x_twitter = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    discord = models.CharField(max_length=200, blank=True, null=True)
    tiktok = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_cliente'

    def __str__(self):
        return f"Cliente Espejo: {self.user.username}"