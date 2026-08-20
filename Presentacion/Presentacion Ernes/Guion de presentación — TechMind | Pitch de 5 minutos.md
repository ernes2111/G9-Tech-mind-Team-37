# Guion de presentación — TechMind

**Duración objetivo: 4:30–4:45 minutos**

---

## 0:00 – 0:45 | Hook + problema

**[Diapositiva: una gran cantidad de documentos, PDFs, tutoriales, apuntes y documentación dispersa.]**

“Quiero empezar con una pregunta.

¿Cuántas veces guardamos un tutorial, una documentación, un PDF o un apunte porque pensamos que algún día lo vamos a necesitar?

Y cuando finalmente lo necesitamos… ya no recordamos dónde estaba.

Ahora imaginemos eso, pero no con diez documentos, sino con cientos o miles.

Estudiantes, desarrolladores, equipos técnicos y empresas generan constantemente conocimiento. El problema es que ese conocimiento crece muchísimo más rápido de lo que podemos organizarlo manualmente.

Y ahí aparece una necesidad muy concreta:

**¿Cómo transformamos todo ese contenido técnico que tenemos disperso en conocimiento que podamos encontrar, entender y reutilizar fácilmente?**

Ese es el problema que buscamos resolver con TechMind.”

**[Pausa breve.]**

---

## 0:45 – 1:30 | Propuesta de valor

**[Diapositiva: “TechMind — Del contenido al conocimiento”]**

“TechMind es una plataforma que **organiza automáticamente contenido técnico utilizando Ciencia de Datos**.

En una sola frase:

**TechMind ayuda a estudiantes, profesionales y organizaciones a transformar contenido técnico desordenado en conocimiento estructurado, sin tener que catalogarlo manualmente.**

¿Cómo funciona?

El usuario puede escribir un contenido técnico o, todavía más simple, subir directamente un PDF o un documento Word.

TechMind analiza ese contenido y automáticamente identifica:

**de qué tema se trata, qué nivel de confianza tiene la clasificación y cuáles son las palabras clave más relevantes.**

Y además guarda ese resultado, para que ese conocimiento pueda consultarse posteriormente.

En lugar de tener simplemente una carpeta llena de documentos, empezamos a construir una **base de conocimiento organizada automáticamente**.”

---

# 1:30 – 3:10 | Demo en vivo

**[Abrir TechMind. Tener preparado un PDF técnico realista.]**

“Y quiero mostrarles cómo funciona esto en la práctica.

Voy a tomar un documento técnico que ya tengo preparado.

En lugar de copiar todo su contenido manualmente, simplemente voy a importarlo.”

**[Click → Importar PDF/DOCX.]**

“TechMind extrae automáticamente el contenido del documento y completa la información por nosotros.”

**[Mostrar título y texto extraído.]**

“Ahora simplemente le pedimos que lo clasifique.”

**[Click → Clasificar con TechMind.]**

“Y en unos segundos obtenemos el resultado.

En este caso, TechMind identifica que este contenido pertenece a **[mostrar categoría que corresponda al documento de demo]**, con una confianza de **[X%]**, y además identifica automáticamente palabras clave como **[mostrar 2 o 3]**.”

**[Pausa breve para que el jurado vea el resultado.]**

“Pero lo importante no es solamente esta clasificación.

El resultado queda almacenado.”

**[Ir a Historial.]**

“Por eso podemos volver posteriormente, buscar por título o palabra clave y filtrar nuestros contenidos por categoría.”

**[Mostrar búsqueda/filtro.]**

“Y cuando ya tenemos suficientes contenidos, podemos empezar a ver cómo se está construyendo nuestra base de conocimiento.”

**[Ir a Analytics.]**

“Por ejemplo, podemos observar qué categorías aparecen con mayor frecuencia, cuáles son las palabras clave más utilizadas y cómo evoluciona la actividad.”

**[Pausa.]**

“Es decir, pasamos de tener documentos aislados…

a tener **información organizada y consultable**.”

---

## 3:10 – 4:10 | Arquitectura, desafíos y por qué destacamos

**[Diapositiva: arquitectura simplificada con 4 bloques. No mostrar código.]**

“Detrás de esta experiencia hay un sistema completo.

Tenemos una aplicación web que recibe el contenido, un servicio encargado del análisis mediante Machine Learning, una API que coordina el procesamiento y una base de datos donde almacenamos los resultados.

El modelo fue entrenado específicamente para contenido técnico y trabaja con ocho categorías, alcanzando un **90,38% de accuracy en nuestro conjunto de prueba**.”

**[Mostrar el dato grande: 90,38%.]**

“Pero para nosotros, uno de los mayores desafíos no fue solamente entrenar el modelo.

Fue conseguir que todo funcionara como un producto real.

Durante el desarrollo tuvimos que resolver problemas de integración, persistencia, manejo de errores y rendimiento. Incluso detectamos un problema que podía agotar las conexiones de la base de datos bajo carga y tuvimos que rediseñar parte del flujo para solucionarlo.

Además realizamos múltiples ciclos de QA, documentando casos de prueba, errores y correcciones.”

**[Pausa.]**

“Y todo esto está preparado para ejecutarse de forma completamente contenerizada y desplegado en Oracle Cloud.”

---

## 4:10 – 4:40 | Cierre memorable + llamada a la acción

**[Diapositiva final: TechMind + frase grande.]**

“Todos los días generamos conocimiento.

El problema es que gran parte de ese conocimiento termina perdido entre documentos, tutoriales, apuntes y archivos que después cuesta volver a encontrar.

**TechMind busca cambiar eso.**

Queremos que organizar conocimiento técnico deje de ser una tarea manual y pase a ser algo automático.

Porque el valor no está solamente en tener información.

**Está en poder encontrarla, entenderla y reutilizarla cuando realmente la necesitamos.**

Eso es TechMind.

**Convertir contenido técnico en conocimiento organizado.**”

**[Pausa. Mirar al jurado.]**

“Muchas gracias.”