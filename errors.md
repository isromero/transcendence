## PROBLEMAS ENCONTRADOS

### TODO ISMA -> NO SE HASHEA LA CONTRASEÑA CUANDO CAMBIAS EL NOMBRE DEL USUARIO ENTONCES SE CAMBIA Y NO PUEDES VOLVER A INICIAR SESIÓN
- Al cambiar el nombre de usuario, se sale de la sesion y ya no deja de acceder, invalid credencial. Y no deja registrarse con el usuario nuevo. 
ejemplo:
Username: user1
New username: user2
No deja loguearse con ninguno
deja registrar a user1 pero no a user2

### TODO (isma): si me da tiempo
- No se puede eliminar amigos, aunque el subject no dice que hay que hacerlo # 

### TODO ISMA
- En multijugador el mismo usuario puede mover las dos flechas.

### TODO ADRI (esto creo que no está mal, el zoom no es algo que importa o pantallas tan dinámicas pero echale un ojo)
- Ajuste dinamico de tamaño de la pagina en vertical. Al hacer zoom se sobreponen las lineas

### TODO SAMU
- Screen reader and assistive technologies. Tenemos esto hecho?

### TODO SAMU
- Los mensajes de error o de confirmación (los que salen arriba a la derecha en rojo o verde) siempre son en inglés independientemente del idioma del usuario.
- También es estadísticas, Tournaments Wins y Tournaments Loses siempre están en inglés

### TODO SAMU
- Revisar con Jose el tema de los ws y http dentro del cli cuando nuestro sistema ahora es WSS y HTTPS
    + El cli se conecta directamente al 8000 y con ws. ¿¿¿Es válido??? Funcionar funciona. 

### TODO ISMA
- SPA navegación hacia atrás OK, pero hacia adelante no se puede (el botón hacia adelante no está habilitado en el navegador. Probado en merge-temp)

### TODO SAMU
- Textos sin traducir cuando no tienes ningún amigo y cuando no te tienes ninguna solicitud de amigo pendiente

### TODO nosequién
- El nombre mostrado al finalizar el torneo no corresponde con el nombre que el usuario ha puesto para jugar el torneo, si no que se muestra el username de registro en la aplicación.
- En la pantalla intermedia del torneo (en la de las semifinales) sí se muestra bien, el fallo únicamente es el la pantalla final del resumen del torneo.

### TODO or not TODO
- Esto es una pijada que no creo que merezca la pena. Tiene que ver con la gestión de amigos.
La secuencia sería la siquiente:
Josgarci manda invitación de amigo a Lyandriy.
Lyandriy manda invitación de amigo a Josgarci.
Josgarci acepta la invitación.
Lyandriy rechaza la invitación.
Josgarci y Lyandriy son amigos.

## TESTEADO EN 42 Y NO SOLUCIONADO






## TESTEADO EN 42 Y FUNCIONAL

### TODO ADRI ✅ Hecho (checkeado en rama merge-temp)
- No deja crear torneos Si habia una vez un jugador que se puso un nombre en un torneo tipo: jugador1, luego en otros torneos no le deja usarlo.
duplicate key value violates unique constraint "core_user_tournament_display_name_321645ac_uniq"
DETAIL: Key (tournament_display_name)=(uno) already exists.

### PROBABLEMENTE ARREGLADO PERO REVISAR 🔔 LYUDMYLA Y SAMU ✅ Hecho (checkeado en rama merge-temp)
- Aveces No deja cambiar de avatar (Error updating avatar) y aveces se queda pillado y no entre en la pagina para cambiar avatar
    + Arreglado (poner en docker compose de be el volumen be_media:/app/media para que lo comparta con caddy y pueda servir las imágenes)

### TODO ISMA ✅ Hecho (checkeado en rama merge-temp)
- No aparecen las estadisticas del torneo.

### TODO ISMA ✅ Hecho (checkeado en rama merge-temp)
- Muestra mal las estadisticas de amigos, en la pagina donde se listan los amigos y en el perfil de amigo se muestran las estadisticas diferentes y no verdaderas. En el perfil del amigo no se muestra si esta online

### PROBABLEMENTE ARREGLADO PERO REVISAR 🔔 LYUDMYLA Y SAMU (checkeado en rama merge-temp)
- En otro ordenador no carga las fotos de perfil
    + Arreglado (poner en docker compose de be el volumen be_media:/app/media para que lo comparta con caddy y pueda servir las imágenes)

### TODO TODOS ✅ Hecho (checkeado en rama merge-temp)
- Lag en el juego en ordenadores de 42

### TODO JOSE ✅ Hecho (checkeado en rama merge-temp)
- Errores callback de la intra
    + Arreglado en rama merge-temp cambiar
    (oauth.py // oauthcallback)     return HttpResponseRedirect(f"http://{settings.OAUTH42_HOSTNAME}:3001/")
                                    return HttpResponseRedirect(f"https://{settings.OAUTH42_HOSTNAME}/")
    Tiene que existir la varible de entorno OAUTH42_HOSTNAME=hostname:8443 o cXrYsZ.42madrid.com:8443

### TODO JOSE ✅ Hecho (checkeado en rama merge-temp)
- Errores de las métricas, no salen nada (y revisar en 42 si da error metrics.js)

### TODO JOSE (checkeado en rama merge-temp)
- Limpiar archivos de grafana obsoletos y dejar solo el dashboard definitivo 

### TODO JOSE (checkeado en rama environmet_unified)
- Unificar las variables de entorno en un único archivo. (subject dice environment variables must be set inside a .env)

