from django.db import models
from django.contrib.auth.models import User


class CanalTransmision(models.Model):
    # Usamos DO_NOTHING para que si borras algo en el público no afecte al panel
    usuario = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="canal_transmision_pub")
    en_vivo = models.BooleanField(default=False)
    
    # IMPORTANTE: Si en el panel agregaste 'url_hls' o 'titulo_stream' después, 
    # agrégalos aquí también. Si solo tienes 'en_vivo', déjalo así.

    class Meta:
        managed = False          # Django no creará ni modificará esta tabla
        db_table = 'core_canaltransmision'  # El nombre real en la base de datos compartida

    def __str__(self):
        return f"Canal de {self.usuario.username}"