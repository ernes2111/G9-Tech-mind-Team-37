# Guion de presentación — TechMind
### Formato: video grabado · vos en cuadro chico + pantalla compartida · 11 estaciones + demo de Ernesto

> Este guion no es para leer. Los slides ahora muestran solo palabras clave — el desarrollo completo de cada idea vive acá, para que vos lo digas con tus palabras mirando a cámara, no a la pantalla. Como es un video grabado y vos grabás tu parte por separado de la de Ernesto (demo), hay notas extra pensadas para que el corte entre los dos quede prolijo en la edición.

---

## 1 · Hero — TechMind

*(Primeros segundos del video — asegurate de que el cuadro de tu cámara ya esté encendido y bien encuadrado antes de arrancar a grabar, así no hay que cortar el inicio.)*

**Decí algo así:**
"Buenas, somos el equipo 37 de G9 LATAM y venimos a mostrarles TechMind. La idea en una frase: es un sistema que lee un texto técnico y solo, sin que nadie lo etiquete a mano, entiende de qué tema habla."

**Transición:** "Y esto nace de un problema bastante común, que seguro varios acá conocen..."

---

## 2 · El problema

*(El slide ahora muestra un ícono dibujado por cada formato — PDF, Word, CSV, Manuales, Docs oficiales, Info web — en vez de una lista de texto. Dejá que el jurado los vea un segundo, funcionan solos, no hace falta nombrarlos uno por uno.)*

**Decí algo así:**
"Piensen en cualquier equipo técnico: la documentación vive repartida en PDFs, Word, planillas, wikis, artículos sueltos. Cuando alguien nuevo entra al equipo, o cuando necesitás encontrar algo puntual, terminás perdiendo un montón de tiempo buscando, o peor: reescribiendo algo que ya existía porque no lo encontraste."

**Enfatizá con tu voz** los 4 síntomas que están en el slide: tiempo perdido, duplicación, no encontrar lo correcto, conocimiento que no se reutiliza — no hace falta leerlos, decilos con tus palabras.

**Transición:** "Entonces nos propusimos resolver eso específicamente..."

---

## 3 · Objetivo y solución

*(El slide ahora solo dice "La documentación correcta, en segundos" y "El sistema lee, aprende y clasifica solo" — nada más, ni siquiera la analogía. Todo el desarrollo lo hacés vos acá.)*

**Decí algo así:**
"El objetivo es simple: que cualquier persona encuentre la documentación correcta en segundos, sin tener que buscar en diez lugares distintos. Y la solución es que el sistema mismo lea cada texto, aprenda de qué tema trata, y lo clasifique automáticamente — sin que una persona tenga que etiquetarlo a mano."

**La analogía (opcional, ya no está ni resumida en el slide — usala si sentís que suma calidez a la explicación):**
"Es como tener un asistente que lee cada documento que entra a la empresa y lo archiva solo en la carpeta correcta, en vez de que alguien tenga que leerlo y decidir dónde va."

**Tip:** si la decís, que sea corta y de pasada — esta es tu frase ancla para repetir más adelante si sentís que perdiste al jurado en la parte técnica, no hace falta extenderte acá.

**Transición:** "Para lograr esto, no armamos un programa gigante que hace todo. Lo dividimos en partes especializadas..."

---

## 4 · Cómo está armado por dentro (arquitectura)

*(El slide muestra 4 cajas con nombres cortos — "la pantalla", "el recepcionista", "el experto en IA", "el archivo" — y ahora también un mini semáforo visual con su explicación básica ya escrita ahí ("verde si funciona, rojo si no"). No hace falta que vos expliques el semáforo desde cero, el slide ya lo hace — solo reforzalo con tu voz.)*

**Decí algo así:**
"Son cuatro partes que se pasan la posta. Primero está la pantalla, donde la persona escribe el texto — eso ya es una aplicación real funcionando, no un mockup. Esa pantalla le manda el pedido a una parte que lo recibe y organiza, como un recepcionista. El recepcionista se lo pasa a la parte que realmente piensa — el motor de Inteligencia Artificial — que analiza el texto y decide la categoría. Y por último, todo eso queda guardado, como un archivo con historial."

**Sobre el semáforo (el slide ya lo explica, esto es solo para reforzar si querés agregar algo):**
"Y como ven ahí, la pantalla tiene un semáforo — les muestra en el momento si cada parte está funcionando, sin que nadie tenga que revisar nada a mano."

**Si preguntan detalles técnicos:** ahí sí mencionás Spring Boot (puerto 8080), FastAPI (puerto 8000) y PostgreSQL (puerto 5432) — están anotados en chiquito en el slide por si hace falta.

**Transición:** "Y para armar esto, elegimos herramientas puntuales para cada tarea..."

---

## 5 · Con qué lo construimos (stack)

*(Slide con frases de 3-4 palabras por herramienta. Es el slide de menor protagonismo — pasalo con ritmo.)*

**Decí algo así:**
"No me detengo mucho acá porque es más para quien le interese el detalle técnico — pero en criollo: una pantalla muestra todo, una herramienta atiende pedidos, otra piensa y clasifica el texto, y la base de datos guarda todo en la nube, no en una sola compu."

**Transición:** "Ahora, lo más interesante: ¿cómo aprende el sistema a clasificar sin que nadie le enseñe caso por caso?"

---

## 6 · Cómo aprende el sistema (pipeline ML)

*(El slide ahora es una lista de 7 palabras clave + el número grande "~69%". Este es el corazón de tu parte — hablalo con calma, es donde más valor agregás vos.)*

**Decí algo así:**
"Es como enseñarle a alguien nuevo en un trabajo. Si le mostrás cien mails ya clasificados como 'reclamo' o 'consulta', después de un rato la persona empieza a reconocer el patrón sola. Acá hicimos lo mismo pero con texto técnico: juntamos muchos ejemplos ya clasificados, limpiamos el texto, identificamos qué palabras son típicas de cada tema, y el sistema aprendió el patrón. Además de la categoría, también identifica las palabras más importantes del texto, así el resultado da más contexto."

**Sobre el ~69% (decilo con estas palabras exactas, es tu frase de honestidad técnica):**
"Hoy el modelo acierta cerca del 69% de las veces, entre 8 categorías posibles. Es un número que va a mejorar: el dataset todavía es chico, unos 60 ejemplos, y sabemos que las categorías con más dificultad son DevOps y Seguridad, justamente las que menos ejemplos tienen. A medida que sumemos más contenido de entrenamiento, ese número sube."

**Por qué decir el número en vez de esconderlo:** un jurado técnico valora mucho más la honestidad con un número real y bajo, que un silencio sospechoso. Mostrar que sabés *por qué* el número es el que es (dataset chico) demuestra que entendés el modelo, no que lo corriste una vez y ya.

**Transición:** "Y para que no quede solo en teoría, les muestro un caso real..."

---

## 7 · Un caso real (ejemplo concreto)

*(Slide nuevo — muestra el JSON real de entrada/salida. Dejá que el jurado lo lea un segundo antes de hablar.)*

**Decí algo así:**
"Este es un caso real: alguien escribe un texto sobre Spring Boot y lo manda a clasificar. El sistema responde en el momento con la categoría — Backend, con 89% de confianza — y además le saca solo las palabras más importantes del texto: spring boot, java, api rest, spring. Nadie tuvo que decirle que esto era de Backend, lo dedujo solo leyendo el contenido."

**Transición:** "Y este equipo detrás de todo esto es..."

---

## 8 · Equipo

**Decí algo así:**
"Somos 8 personas divididas en tres frentes: ciencia de datos, backend, y control de calidad — más toda la parte de infraestructura en la nube que armamos entre todos."

**No leas los nombres uno por uno**, salvo que el jurado lo pida. Con nombrar los frentes alcanza; los nombres quedan visibles en pantalla.

**Transición:** "Y antes de mostrarles que esto funciona, quiero mostrarles que lo probamos a fondo..."

---

## 9 · Control de calidad (QA)

*(Slide con el "100%" grande y "38 pruebas realizadas, todas aprobadas" — sin mencionar sprints ni la analogía del auto, que ya no están en pantalla. Este es tu momento más fuerte de toda la charla — bajá el ritmo acá, dejá que el número respire.)*

**Decí algo así:**
"Acá tenemos el dato más contundente de toda la presentación: corrimos 38 pruebas distintas sobre el sistema — funcionamiento, casos límite, seguridad, validación de datos, resistencia a ataques — y las 38 pasaron. 100% de éxito. Probamos desde que clasifique bien, hasta que aguante 100 pedidos al mismo tiempo, hasta que resista intentos de ataque como inyección SQL y XSS."

**Si te preguntan cómo se dividieron esas 38 pruebas (dato de respaldo, no hace falta decirlo si nadie pregunta):**
"Fueron en dos rondas: 24 pruebas en una primera etapa, cubriendo lo funcional y la seguridad básica, y 14 más después, enfocadas en resistencia a ataques más específicos y en cómo se recupera el sistema ante fallos."

**Pausa después de decir "100%".** Dejá que el número respire un segundo antes de seguir con el resto.

**Transición:** "Con esto funcionando, ya pensamos hacia dónde va el proyecto después del hackathon..."

---

## 10 · Roadmap

*(Slide actualizado — ya no dice "vamos a hacer" para todo, ahora distingue lo que ya está hecho de lo que sigue.)*

**Decí algo así:**
"Hoy ya tenemos la clasificación funcionando de punta a punta, el frontend en producción, y algo que antes era plan y ahora ya es realidad: el sistema puede leer directamente PDFs y Word, no solo texto pegado a mano. Lo que estamos discutiendo en este sprint es sumar un módulo de usuarios y contraseñas, para que cada contenido quede asociado a quién lo subió. Después, el siguiente paso es que el sistema baje documentación oficial de internet automáticamente. Y la visión final es una base de conocimiento que se actualiza sola, sin que nadie tenga que cargar nada a mano."

**Transición:** "Y con esto, les queremos mostrar el sistema funcionando en vivo."

---

## 11 · Cierre

*(Acá termina tu parte grabada. Como Ernesto graba la demo por separado, esta frase es el "gancho" que el editor va a usar para cortar de tu clip al de él — decila completa y clara, sin cortarte, para que el corte quede prolijo.)*

**Decí algo así:**
"Así que eso es TechMind: conocimiento técnico disperso, ordenado automáticamente por Inteligencia Artificial, probado a fondo con 38 pruebas, y con una visión clara de hacia dónde crece. Ahora le paso la posta a Ernesto, que les va a mostrar TechMind funcionando en vivo."

**Después de decir esta frase, quedate en silencio y en cuadro 2-3 segundos antes de cortar la grabación.** Le da al editor un margen limpio para hacer el corte a la parte de Ernesto, en vez de que la frase quede pegada de golpe a su clip.

**Coordinación con Ernesto:** convendría que él arranque su parte con una frase que "conecte" con esta, tipo "Gracias Romulo, les muestro cómo funciona" — si no lo tienen hablado todavía, valdría la pena confirmarlo antes de grabar, para que no quede una transición seca en la edición.

---

## 12 · Demo en vivo (Ernesto) — PENDIENTE DE COMPLETAR

> Romulo: esta sección es un esqueleto. Faltan los detalles específicos porque todavía no corrimos el programa. Complétenla juntos (o que Ernesto la complete y te la mande de vuelta) apenas alguno de los dos pruebe la app funcionando.

**Gancho de entrada (conecta con el cierre de Romulo):**
"Gracias Romulo, les muestro cómo funciona TechMind en la práctica."

**Estructura sugerida para la demo — completar con lo que realmente se vea en pantalla:**

1. **Mostrar la pantalla principal** — [ ] Describir brevemente qué se ve al entrar (el formulario de título/contenido, el semáforo de estado de los 3 servicios)
2. **Clasificar un texto en vivo** — [ ] Elegir 1-2 textos técnicos de ejemplo (idealmente distintos entre sí, ej. uno de Backend y uno de Data Science, para mostrar que discrimina bien entre categorías)
3. **Mostrar el resultado** — [ ] Señalar categoría, porcentaje de confianza y palabras clave en pantalla
4. **(Opcional) Mostrar el historial** — [ ] Si el historial de contenidos clasificados recientemente se ve bien, mostrarlo como prueba de que no es la primera vez que anda
5. **Cierre de la demo** — [ ] Frase final del video, agradeciendo o invitando a preguntas

**Preguntas para resolver antes de grabar esta parte:**
- ¿Qué 1-2 textos de ejemplo va a usar Ernesto? (conviene que no sean los mismos que ya mostramos en el slide "Un caso real", para no repetir)
- ¿La demo va a mostrar algún error o caso límite a propósito (para lucir la robustez que probó QA), o solo el camino feliz?
- ¿Cuánto dura esta parte? Afecta si el video total queda muy largo sumado a las 11 estaciones previas.

**Nota de continuidad con el resto del video:** el tono de Ernesto debería sentirse como una continuación natural, no un video aparte — recomendable que arranque con energía similar a como termina Romulo (ver tips de coordinación en la sección de Tips generales, más abajo).

- **Los slides ahora son solo palabras clave a propósito** — están para que quien mira el video lea rápido y te preste atención a vos, no para que los leas vos mismo. El desarrollo completo de cada idea está en este guion.
- **Mirá al lente de la cámara, no a la pantalla ni al guion.** Como estás en un cuadro chico superpuesto a la ppt, mirar a cámara es lo que da sensación de contacto visual con quien ve el video después — mirar la pantalla se nota como "estar leyendo".
- **Grabá con margen al principio y al final de tu clip** (2-3 segundos de silencio en cuadro, sin hablar) — le da aire al editor para cortar prolijo, tanto al arrancar como en el traspaso a Ernesto al final.
- **Si te trabás o no te convence una toma, cortá y volvé a grabar esa sección entera**, no intentes arreglarlo hablando de más — es más fácil elegir la mejor toma completa que editar a mitad de frase.
- **Chequeá el audio antes de grabar todo** (una toma corta de prueba) — en un video grabado, un audio con eco o volumen bajo pesa más que en una presentación en vivo, porque no hay forma de "corregir" preguntando de nuevo.
- **Tus dos momentos fuertes son el slide 6 (accuracy ~69%, decilo con seguridad, no te disculpes por el número) y el slide 9 (QA 100%, bajá el ritmo ahí)** — en un video grabado, esos son los puntos donde más vale la pena regrabar si la primera toma no te convence.
- **Coordiná con Ernesto el tono de energía** antes de grabar — si tu cierre queda muy pausado y su arranque de demo es muy acelerado (o al revés), el corte se nota raro. Una llamada rápida de 5 minutos comparando cómo van a sonar alcanza.
