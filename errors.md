### TODO ISMA -> NO SE HASHEA LA CONTRASEÑA CUANDO CAMBIAS EL NOMBRE DEL USUARIO ENTONCES SE CAMBIA Y NO PUEDES VOLVER A INICIAR SESIÓN
- Al cambiar el nombre de usuario, se sale de la sesion y ya no deja de acceder, invalid credencial. Y no deja registrarse con el usuario nuevo. 
ejemplo:
Username: user1
New username: user2
No deja loguearse con ninguno
deja registrar a user1 pero no a user2


### TODO ADRI
- No deja crear torneos Si habia una vez un jugador que se puso un nombre en un torneo tipo: jugador1, luego en otros torneos no le deja usarlo.
duplicate key value violates unique constraint "core_user_tournament_display_name_321645ac_uniq"
DETAIL: Key (tournament_display_name)=(uno) already exists.

### TODO ADRI (no sé si esto realmente está o no)
- No aparecen las estadisticas del torneo.

### TODO ISMA (aunque lo de que no salga online da un poco igual)
- Muestra mal las estadisticas de amigos, en la pagina donde se listan los amigos y en el perfil de amigo se muestran las estadisticas diferentes y no verdaderas. En el perfil del amigo no se muestra si esta online

### PROBABLEMENTE ARREGLADO PERO REVISAR 🔔 LYUDMYLA Y SAMU
- Aveces No deja cambiar de avatar (Error updating avatar) y aveces se queda pillado y no entre en la pagina para cambiar avatar 

### TODO (isma): si me da tiempo
- No se puede eliminar amigos, aunque el subject no dice que hay que hacerlo # 

### PROBABLEMENTE ARREGLADO PERO REVISAR 🔔 LYUDMYLA Y SAMU
- En otro ordenador no carga las fotos de perfil
    + Arreglado (poner en docker compose de be el volumen be_media:/app/media para que lo comparta con caddy y pueda servir las imágenes)

### TODO ISMA
- En multijugador el mismo usuario puede mover las dos flechas.

### TODO ADRI (esto creo que no está mal, el zoom no es algo que importa o pantallas tan dinámicas pero echale un ojo)
- Ajuste dinamico de tamaño de la pagina en vertical. Al hacer zoom se sobreponen las lineas

### TODO SAMU
- Screen reader and assistive technologies. Tenemos esto hecho?
- (SAMU:) si eso ya lo tenemos!

### TODO TODOS
- Lag en el juego en ordenadores de 42
   

### TODO JOSE 
- Errores callback de la intra
    + Arreglado en rama merge-temp cambiar
    (oauth.py // oauthcallback)     return HttpResponseRedirect(f"http://{settings.OAUTH42_HOSTNAME}:3001/")
                                    return HttpResponseRedirect(f"https://{settings.OAUTH42_HOSTNAME}/")
    Tiene que existir la varible de entorno OAUTH42_HOSTNAME=hostname:8443 o cXrYsZ.42madrid.com:8443


### TODO JOSE
- Errores de las métricas, no salen nada (y revisar en 42 si da error metrics.js)

### TODO SAMU
- Revisar con Jose el tema de los ws y http dentro del cli cuando nuestro sistema ahora es WSS y HTTPS
- esto ya lo tenemos, no podemos cargarnos el localhost 8000 porque no solo se necesita para el cli si no para otra cosas de lo que me ha comentado jose
