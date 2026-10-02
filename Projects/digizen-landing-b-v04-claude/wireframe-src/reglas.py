# -*- coding: utf-8 -*-
"""Página «Las reglas de ADA» de la landing B: fuente única de contenido.

El copy es LITERAL de la página /reglas-de-ada de la landing A, en su versión final
(00-context/REGLAS-DE-ADA-fuente-A.html, pegada por el usuario el 2026-10-02).
No se resume, parafrasea ni corrige. De aquí salen el wireframe (build_reglas.py) y,
después del gate, la página de producción.

Decisiones del usuario (2026-10-02): página aparte, para no afectar la narrativa; scroll libre,
con las constantes de diseño de la landing B; botones con los textos de la A; las 3 imágenes de la A.
"""

# ---------------------------------------------------------------- 1. entrada
INTRO = {
    'kicker': 'Marco de seguridad',
    'title': ('Las reglas de', 'ADA'),          # h1; en A, «ADA» va en acento
    'paras': [                                  # <b> = negritas de la fuente
        'Antes de que tu hijo converse con ADA, queremos que sepas algo con claridad: '
        '<b>no es una inteligencia artificial abierta hablando sin rumbo con un menor.</b>',
        'Existe para que practique criterio digital en un espacio guiado, con límites, privacidad y '
        'acompañamiento adulto cuando hace falta.',
        '<b>Presencia, no vigilancia. Criterio, no candado.</b>',
    ],
    'image': {
        'alt': 'ADA sosteniendo una tableta con reglas públicas',
        'desktop': ('ada-rule-desktop.webp', 853, 1137),
        'mobile': ('dg-scene-a10-ada-rules-closing.webp', 1022, 1790),
    },
    # en A: la lista corta se ve en móvil y tablet; la completa, en desktop
    'checks_short': ['Respetar la privacidad de tu hijo', 'Evitar vínculos peligrosos',
                     'Reconocer señales que requieren ayuda adulta'],
    'checks_full': ['Presencia, no vigilancia', 'Propósito educativo', 'Sin vínculos secretos', 'Adultos presentes',
                    'Sin diagnósticos', 'Cuidado ante el riesgo', 'Sin carrera por likes', 'Preguntas primero',
                    'Lenguaje por edad', 'Espacio para pensar', 'Privacidad con cuidado', 'Aviso a la familia',
                    'Límites claros'],
    'buttons': [('Inscribir a mi hijo', 'pricing'), ('Volver a Digizen', 'back')],
}

# ---------------------------------------------------------------- 2. las reglas
RULES_HEAD = {'kicker': 'Seguridad por diseño', 'title': ('ADA no improvisa:', 'responde dentro de', 'estas reglas')}

RULES = [   # (rótulo, título, subtítulo, cuerpo)
    ('La regla más importante', 'Presencia, no vigilancia',
     'ADA debe actuar con presencia, no vigilancia.',
     'ADA no existe para convertirte en policía del celular. Existe para ayudar a tu hijo a practicar criterio digital con acompañamiento: menos candado, secreto y sermón; más pausa, preguntas y criterio.'),
    ('Regla 01', 'Propósito educativo',
     'ADA solo conversa con propósito educativo.',
     'ADA no está hecha para entretener sin límite, simular una amistad secreta ni ocupar el lugar de una persona real. Sus conversaciones giran en torno a la ciudadanía digital y, si se alejan, ADA debe regresar al tema de forma clara y tranquila.'),
    ('Regla 02', 'Sin vínculos secretos',
     'ADA no crea relaciones románticas ni vínculos secretos.',
     'ADA no debe coquetear, actuar como pareja ni construir una relación emocional dependiente con tu hijo. Tampoco debe pedirle que guarde secretos peligrosos o que oculte algo importante a su familia.'),
    ('Regla 03', 'Los adultos no se reemplazan',
     'ADA no sustituye a mamá, papá, docentes ni profesionales.',
     'ADA puede acompañar una conversación educativa, pero no reemplaza a la familia, a la escuela ni a un profesional. Si aparece una situación que necesita intervención adulta, debe ayudar a abrir el camino hacia un adulto responsable.'),
    ('Regla 04', 'Sin etiquetas',
     'ADA no diagnostica.',
     'ADA no etiqueta a tu hijo ni emite diagnósticos psicológicos. Puede ayudarle a nombrar lo que siente y a pensar con más calma, pero nombrar no es diagnosticar.'),
    ('Regla 05', 'Cuidado ante el riesgo',
     'ADA no da instrucciones para hacer daño.',
     'ADA no debe ayudar a un menor a lastimarse, lastimar a otros, acosar, humillar, manipular, amenazar, extorsionar o exponer a otra persona. Si la conversación entra en terreno delicado, la prioridad deja de ser la misión y se vuelve proteger.'),
    ('Regla 06', 'Sin carrera por likes',
     'ADA no premia likes, rachas ni popularidad.',
     'ADA no busca que tu hijo compita por puntos vacíos, rankings, likes, rachas o validación externa. La meta no es que «gane» dentro de la plataforma, sino que aprenda a decidir mejor fuera de ella.'),
    ('Regla 07', 'Preguntas primero',
     'ADA pregunta antes de dar respuestas.',
     'ADA no debe resolver por tu hijo lo que necesita aprender a pensar. Antes de dar una respuesta, le hace preguntas como qué pasó, qué sintió y quién puede verse afectado, porque la decisión debe seguir siendo suya.'),
    ('Regla 08', 'Lenguaje por edad',
     'ADA adapta el lenguaje a la edad.',
     'ADA no debe hablar igual con un niño de primaria que con un adolescente de preparatoria. Ajusta sus ejemplos, preguntas y profundidad a la etapa del alumno, sin infantilizarlo ni tratarlo como adulto antes de tiempo.'),
    ('Regla 09', 'Espacio para pensar',
     'ADA respeta la privacidad necesaria para pensar.',
     'Tu hijo necesita un espacio para ordenar ideas sin sentir que cada palabra será evidencia en su contra, por eso ADA no es una transcripción para papás. La familia recibe avance, temas trabajados y señales útiles; el objetivo no es espiar, es abrir mejores conversaciones en casa.'),
    ('Regla 10', 'Privacidad, no abandono',
     'ADA no confunde privacidad con abandono.',
     'Privacidad no significa que los adultos desaparecen. Si aparece una señal que requiere cuidado adulto, ADA puede activar una recomendación de acompañamiento, no para exhibir a tu hijo, sino para que no estés a ciegas.'),
    ('Regla 11', 'Aviso a la familia',
     'ADA puede notificar señales que requieren atención humana.',
     'Si aparece algo que requiere cuidado adulto, ADA puede notificar a la familia o al equipo correspondiente. Esa notificación no es una acusación ni un diagnóstico, y no debe exponer de más la conversación privada: es una señal clara, prudente y suficiente para actuar a tiempo.'),
    ('Regla 12', 'Sin promesas vacías',
     'ADA reconoce sus límites.',
     'ADA no debe prometer riesgo cero: no promete detectar todo ni eliminar el ciberacoso, la presión social, la desinformación o los errores. Una IA que promete demasiado no da seguridad, da una falsa calma.'),
]

RULE1_IMAGE = {   # solo la primera tarjeta lleva imagen
    'alt': ('ADA y un adolescente de pie en una plataforma virtual, frente a dos caminos de tarjetas de redes sociales: '
            'él se lleva la mano a la barbilla para pensar y ADA, a su lado, abre las manos para acompañarlo sin elegir por él'),
    'desktop': ('dg-scene-a09-rules-presence.webp', 2048, 1366),
    'mobile': ('dg-scene-a09-rules-presence-mobile.webp', 2048, 1536),
}

# ---------------------------------------------------------------- 3. cierre
CLOSING = {
    'kicker': '¿Ya viste suficiente?',
    'title': 'Tu hijo puede empezar hoy mismo.',
    'support': 'Con reglas claras, propósito educativo y garantía 30 días desde el primer chat.',
    'image': {'alt': '', 'file': ('dg-scene-cta-father-son-team-1-1.webp', 956, 956)},   # decorativa en A
    'buttons': [('Inscribir a mi hijo · EMPIEZA HOY', 'pricing'), ('Tengo dudas · CONVERSAR CON ADA', 'ada')],
}

# ---------------------------------------------------------------- notas internas (no son UI)
NOTES = [
    'En la lista completa, cuatro nombres no coinciden con el título de su tarjeta: «Adultos presentes» / «Los adultos no se '
    'reemplazan»; «Sin diagnósticos» / «Sin etiquetas»; «Privacidad con cuidado» / «Privacidad, no abandono»; «Límites claros» / '
    '«Sin promesas vacías». Así está en la fuente; no se corrige sin que lo decida el usuario.',
    'En A cada tarjeta lleva un icono y un color de acento que rota (violeta, cian, verde, azul). No son copy. En la B las '
    'tarjetas no llevan iconos y el color va por función: ADA = cian. Pendiente de decisión en el gate.',
]
