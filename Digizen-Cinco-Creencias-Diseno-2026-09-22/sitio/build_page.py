from pathlib import Path
import re,html,json
source=Path('copy-source.md').read_text()
page=source.split('## LA PÁGINA',1)[1].split('## Notas de producción',1)[0]
# Keep the rules link functional when the copy spells out its label.
page=page.replace('*Conocer las Reglas de ADA ↗*','[REGLAS]')
# Keep the supplied narrative; translate internal vocabulary into family language.
replacements={
 'Antes de seguir: no eres mal papá.':'Antes de seguir: no eres mala mamá ni mal papá.',
 'Los microcursos de Gnius Club para papás.':'Los cursos breves de Gnius Club para mamás y papás.',
 'los microcursos para papás que van incluidos':'los cursos breves para mamás y papás que van incluidos',
 'Tu instinto no está roto. Está calibrado para un problema que no es éste.':'Tu instinto no está roto. Te ayudó a resolver otros problemas. Éste necesita algo distinto.',
 'Suéltate la culpa. La vas a necesitar libre para lo que sigue.':'Suéltate la culpa. Necesitas espacio para lo que sigue.',
 'plataforma de Digizen':'página de Digizen',
 'un curso-bot que suelta tareas':'un robot que suelta tareas',
 'por qué el feed lo jala, qué siente antes y después de scrollear':'por qué le cuesta dejar de ver videos, qué siente antes y después de pasar un rato en redes',
 '«yo soy el feed» a «yo no soy el feed; lo uso a mi favor»':'«lo que veo en redes me dice quién soy» a «yo decido qué me sirve y qué quiero compartir»',
 'auditar a la IA de tu hijo':'conocer a la inteligencia artificial con la que hablará tu hijo',
 'contigo en el circuito':'con tu participación',
 '**Tú estás en el circuito.**':'**Tú también participas.**',
 '**Con límites de sesión por diseño.**':'**Con un tiempo definido para cada conversación.**',
 '**Tu boleta de progreso.**':'**Un resumen de su avance.**',
 'el feed no sale de vacaciones':'las redes no salen de vacaciones',
 'El curso de competencias de IA para profesionistas':'El curso para aprender a usar inteligencia artificial en tu trabajo',
 'Nadie más en este mercado te deja conocer a la inteligencia artificial con la que hablará tu hijo antes de pagar. Nosotros la ponemos por delante.':'Queremos que conozcas a la inteligencia artificial con la que hablará tu hijo antes de pagar. Por eso la ponemos por delante.',
 'Un mentor así es imposible con humanos a cualquier precio; hoy es posible gracias a la IA.':'Un espacio para conversar, hacer preguntas y practicar decisiones con ayuda de la inteligencia artificial.',
 '**Y una garantía que nadie más da:**':'**Y nuestra garantía:**',
 'Hay algo que ninguna otra actividad de tu hijo puede ofrecerte:':'Hay algo que hace más sencillo empezar:',
 'Tu hijo no te está desobedeciendo. Se está defendiendo. Igual que tú hace tres renglones.':'Quizá no sea solo desobediencia. Puede estar defendiéndose. Igual que tú hace unos renglones.',
 '**nadie aprende nada mientras se defiende.**':'**qué difícil es aprender cuando estamos a la defensiva.**',
 'Lo acabas de comprobar tú mismo, con este texto, hace treinta segundos.':'Quizá acabas de reconocerlo tú mismo al leer este texto.',
 'Es que cada orden le llega como un ataque.':'Puede que esté recibiendo tus palabras como un ataque.',
 'Ya sabes que con órdenes no entra nada.':'Ya viste lo difícil que es escuchar cuando uno está a la defensiva.',
 'Hoy sentiste dos veces la cosita en el pecho.':'Quizá hoy sentiste dos veces la cosita en el pecho.',
}
for a,b in replacements.items():page=page.replace(a,b)
page=page.replace('Las tragedias que has visto en las noticias pasaron en apps de compañeros románticos de rol, diseñadas para engancharlo sin límite. La categoría que los expertos declararon inaceptable para menores, y que hasta sus propios fabricantes ya cerraron a menores de 18.','Hay aplicaciones que simulan amistades o relaciones románticas. Common Sense Media advirtió en 2025 que los compañeros de inteligencia artificial presentaban riesgos inaceptables para menores. ADA tiene un propósito educativo: ayudarle a pensar y a tomar sus propias decisiones. No está planteada como pareja, terapeuta ni sustituto de las personas que lo acompañan.')
# No invented live destinations: these actions open clearly labelled review flows.
page=page.replace('Déjanos tus datos y te mandamos tu acceso en un minuto, al correo o a tu WhatsApp.','Pide tu acceso al final de esta página para conversar tú con ADA antes de inscribir a tu hijo.')
page=page.replace('Regrésate tres renglones, a donde dice que el candado no sirve.','Acuérdate de lo que acabas de leer sobre el candado.')
page=page.replace('Igual que tú hace tres renglones.','Igual que tú hace un momento.')
# Keep this reveal on its own line, as requested, even when it shares a source paragraph.
page=page.replace(' **El control caduca. El criterio no.**','\n\n**El control caduca. El criterio no.**')
sections=re.split(r'<!--\s*(\d+)\s*·.*?-->',page)
assets={0:('01-cena-absorto.png','Mamá y papá cenan mientras su hijo está absorto en el celular.'),2:('02-candados.png','Cuatro candados abiertos y un oído, como símbolo de escuchar.'),3:('03-escudos-mama.png','Mamá e hijo, cada uno detrás de un escudo idéntico.'),5:('04-calle-mama.png','Una mamá acompaña a su hijo a mirar antes de cruzar una calle representada como publicaciones digitales.'),8:('05-reglas.png','Una hoja en el refrigerador, junto a un dibujo y una lista de compras.'),10:('06-mesa.png','Papá e hijo se miran a la mesa, con los dos teléfonos boca abajo.'),12:('07-cruzar-mochila.png','Un adolescente con mochila cruza mirando hacia adelante. Su papá lo observa desde atrás, sin celular.')}
def scroll_cue():
 return '<div class="scroll-cue" role="img" aria-label="Sigue leyendo hacia abajo"><svg viewBox="0 0 28 40" width="28" height="40" aria-hidden="true"><path d="m5 13 9 9 9-9M5 24l9 9 9-9"/></svg></div>'
def figure(src,alt,eager=False,extra=''):
 return f'<figure class="vignette {extra}"><img src="assets/{src}" width="1536" height="1024" loading="{"eager" if eager else "lazy"}" alt="{alt}"></figure>'
def inline(s):
 s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',s)
 s=s.replace('[REGLAS]','<button class="text-button" type="button" data-open="rules-dialog">Conocer las reglas de ADA ↗</button>')
 return s
chat='''<figure class="chat"><figcaption><span class="avatar">a</span><div><strong>Una pregunta que abre otra puerta</strong><small>Conversación de ejemplo</small></div></figcaption><div class="bubble ada"><small>ADA</small><p>Antes de decidir si la compartes: ¿qué crees que siente la persona de la foto?</p></div><div class="bubble child"><small>HIJO</small><p>Pues pena. Pero yo no la tomé.</p></div><div class="bubble ada"><small>ADA</small><p>Es cierto. ¿Y qué cambia para él si tú la mandas a otro grupo?</p></div><div class="bubble child"><small>HIJO</small><p>Que la ve más gente. Yo también lo estaría haciendo más grande.</p></div></figure>'''
ctas='''<div class="actions"><button class="button primary" type="button" data-open="checkout-dialog">Inscribir a mi hijo <span aria-hidden="true">↗</span></button><button class="button secondary" type="button" data-open="ada-dialog">Conversar con ADA primero</button></div>'''
output=[]
for i in range(1,len(sections),2):
 n=int(sections[i]);body=sections[i+1].strip();blocks=re.split(r'\n\s*\n',body)
 cls='cover' if n==0 else 'panel'
 if n in [3,6,9,12]:cls+=' special'
 if n==4:cls+=' relief'
 if n==11:cls+=' offer'
 out=[f'<section class="{cls}" id="{"inscripcion" if n==11 else "capitulo-"+str(n)}" data-chapter="{n}">']
 if n==0:out.append('<p class="kicker">UNA HISTORIA PARA LEER SIN PRISA</p>')
 action_done=False
 for k,block in enumerate(blocks):
  block=block.strip()
  if not block or block=='---':continue
  if block.startswith('### '):
   tag='h1' if n==0 else 'h2';title=block[4:]
   if n==0:title=title.replace('cinco cosas','*cinco cosas*')
   out.append(f'<{tag}>{inline(title)}</{tag}>');continue
  if block=='[PAUSA]':
   if n in [7,11]:continue
   nxt=blocks[k+1].strip() if k+1<len(blocks) else ''
   full=nxt.startswith('**La cinco.')
   out.append(f'<div class="pause {"long-pause" if full else ""}" aria-hidden="true"></div>');continue
  if block.startswith('[VIÑETA:'):
   if n==7:out.append(chat)
   elif n in assets:
    src,alt=assets[n];out.append(figure(src,alt,n==0))
    if n in [0,2,3,8,10]:out.append(scroll_cue())
   continue
  if block=='[ESTUDIO]':
   out.append('<p class="source-note">Fuente: <a href="https://www.commonsensemedia.org/research/talk-trust-and-trade-offs-how-and-why-teens-use-ai-companions" target="_blank" rel="noopener noreferrer">Common Sense Media, 2025</a>. Encuesta a adolescentes de 13 a 17 años en Estados Unidos.</p>');continue
  if block.startswith('*(Ancla discreta'):
   out.append('<p class="quiet-anchor"><a href="#inscripcion">Si ya viste suficiente, la inscripción está al final de esta página ↓</a><br>Si no, sigue leyendo; falta lo más importante.</p>'+scroll_cue());continue
  if '[ INSCRIBIR' in block or '[ 💬' in block:
   if not action_done:out.append(ctas);action_done=True
   continue
  if block.startswith('|'):
   out.append('''<div class="pricing"><article><p class="kicker">TODO HOY, DE UNA VEZ</p><h3>Precio fundador</h3><p class="price">$4,990 <span>MXN</span></p><p>Te ahorras $1,000 por pagarlo completo.</p><p class="price-detail">Vale hasta el 31 de octubre de 2026.</p><p>Tu hijo empieza hoy.<br>Sin cargos después.</p></article><article><p class="kicker">EN 10 PAGOS MENSUALES</p><h3>Los mismos $5,990</h3><p class="price">$599 <span>MXN × 10</span></p><p>El ciclo completo, dividido en diez.</p><p class="price-detail">Terminas de pagar en el mes diez.<br>ADA sigue con tu hijo hasta el doce.</p><p>Tu hijo empieza hoy.<br>No es una suscripción.</p></article></div>''');continue
  if block.startswith('- '):
   out.append('<ul class="benefits">'+''.join('<li>'+inline(x[2:])+'</li>' for x in block.splitlines() if x.startswith('- '))+'</ul>');continue
  if '\n- ' in block:
   intro,lis=block.split('\n',1);out.append('<p>'+inline(intro)+'</p>');out.append('<ul class="benefits">'+''.join('<li>'+inline(x[2:])+'</li>' for x in lis.splitlines() if x.startswith('- '))+'</ul>');continue
  if n==1 and re.match(r'\*\*(Uno|Dos|Tres|Cuatro|Cinco)\.',block):
   num={'Uno':'01','Dos':'02','Tres':'03','Cuatro':'04','Cinco':'05'};m=re.match(r'\*\*(\w+)\.\*\* (.*)',block,re.S)
   out.append(f'<div class="belief"><span>{num[m[1]]}</span><p>{inline(m[2])}</p></div>');continue
  if block.startswith(('**La cinco.**','**Alguien les dijo')) or block=='**El control caduca. El criterio no.**':
   c='revelation compact-reveal' if block.startswith('**La cinco.**') else 'revelation connected-reveal'
   out.append(f'<p class="{c}">'+inline(block)+'</p>')
   continue
  c=''
  if n==0:
   if block=='Cuatro son falsas.':c='cover-punch'
   elif block.startswith('*'):c='reading-note'
   else:c='cover-tease'
  if block in ['Eres tú.','Esa cara.','Habla tú con ADA primero.']:c='big-line'
  if block.startswith('**«'):c='argument'
  if block.startswith(('**Y nuestra garantía','**Y una garantía')):c='guarantee'
  if block=='Ahora te digo cuál es la verdad.':c='centered-line'
  if block.startswith(('No siente lo mismo que tú.','Y ahí está el problema práctico:')):c='connected-lead'
  if block.startswith('Pero no por lo que crees.'):c='reveal-followup'
  out.append(f'<p class="{c}">'+inline(block).replace('\n','<br>')+'</p>')
  if block=='Los ojos al techo. En señal de fastidio.':
   out.append(figure('08-fastidio-cejas.png','El hijo levanta los ojos al techo con fastidio. El celular que sostiene tapa la parte inferior de su cara.',extra='closeup'))
   out.append(scroll_cue())
  if block.startswith(('Pero no por lo que crees.','Suéltate la culpa.','Ahora te digo cuál es la verdad.','Ese día, lo único que va a cruzar','Pero sí hay alguien que puede estar ahí')):out.append(scroll_cue())
 out.append('</section>');output.append('\n'.join(out))
head=Path('dist/index.html').read_text().split('<body>',1)[0]+'<body>'
header='<a class="skip" href="#historia">Ir a la historia</a><div class="reading-progress" aria-hidden="true"></div><header class="masthead"><span class="brand">digi<b>zen</b><i aria-hidden="true">✳</i></span><span class="edition">CINCO CREENCIAS · UNA CONVERSACIÓN</span></header>'
footer='''<footer class="footer"><div class="faq"><h2>Por si te quedó una duda.</h2><details><summary>¿Para qué edades es Digizen?</summary><p>De tercero de primaria a tercero de preparatoria. Tu hijo arranca en el primer nivel de su sección (primaria, secundaria o prepa) y cada año sube uno. Los temas están pensados para su etapa y para lo que usa a su edad.</p></details><details><summary>¿Qué hace mi hijo cada semana?</summary><p>Una semana ADA le trae un tema nuevo, pensado para su etapa (para él, una misión). La siguiente, lo pone a prueba con una situación real. Son veinte temas a lo largo del ciclo. Y entre semana, ADA está para lo que traiga: algo raro que le mandaron, un juego que le pidió dinero, una duda de si algo es cierto.</p></details><details><summary>¿Voy a poder leer todo lo que habla mi hijo con ADA?</summary><p>Recibes su avance, los temas que ha visto y un resumen que él revisa antes de compartirlo contigo. No recibes una copia de toda la conversación. Antes de empezar se explican los avisos ante situaciones que puedan necesitar ayuda de un adulto.</p></details><details><summary>¿Hay que pagar inscripción y además mensualidades?</summary><p>No. El ciclo completo cuesta $5,990 y es un solo precio, sin cuota de inscripción aparte. Lo pagas todo hoy ($4,990 con el precio fundador) o en diez pagos mensuales de $599. Nunca las dos cosas.</p></details><details><summary>¿Los diez pagos son una suscripción?</summary><p>No. Son los mismos $5,990 divididos en diez. Terminan en el mes diez; ADA sigue con tu hijo hasta el doce.</p></details><details><summary>¿Cómo funciona la garantía?</summary><p>Pruébalo un mes. Los 30 días cuentan desde la primera conversación de tu hijo con ADA, no desde que pagas. Si no es para ustedes, cancelas en un clic y no pagas. Sin llamadas de venta.</p></details><details><summary>¿Puedo conocer a ADA antes de pagar?</summary><p>Sí, el recorrido contempla que tú converses con ADA primero. Usa el botón «Conversar con ADA primero» al final de la historia para ver la solicitud de acceso.</p></details></div><div class="footer-bottom"><span class="brand">digi<b>zen</b></span><p>Presencia, no vigilancia.<br>Criterio, no candado.</p><div><a href="https://gnius.club/" target="_blank" rel="noopener noreferrer">Gnius Club ↗</a><a href="https://gnius.club/aviso-de-privacidad.html" target="_blank" rel="noopener noreferrer">Aviso de privacidad</a><small>© 2026 Gnius Club</small></div></div></footer>'''
modals='''<dialog id="checkout-dialog" aria-labelledby="checkout-title"><button class="close" type="button" data-close aria-label="Cerrar inscripción">×</button><p class="kicker">CICLO DIGIZEN · 12 MESES · $5,990</p><h2 id="checkout-title">Un solo precio. Elige cómo pagarlo.</h2><form id="checkout-form"><fieldset><legend class="sr-only">Forma de pago</legend><label class="payment-choice"><input type="radio" name="payment" value="contado" checked><span><strong>Todo hoy · $4,990 MXN</strong><small>Te ahorras $1,000. Precio fundador hasta el 31 de octubre de 2026.</small></span></label><label class="payment-choice"><input type="radio" name="payment" value="mensualidades"><span><strong>10 pagos mensuales de $599 MXN</strong><small>Los mismos $5,990, divididos en diez. Sin cuota de inscripción aparte.</small></span></label></fieldset><p class="review-note">Versión de revisión: el pago todavía no está conectado. No se hará ningún cargo.</p><button class="button primary" id="pay-button" type="submit">Continuar con la inscripción ↗</button><p class="form-status" id="checkout-status" role="status"></p></form><a class="support" href="https://wa.me/522218481116?text=Hola%2C%20quiero%20informaci%C3%B3n%20sobre%20la%20inscripci%C3%B3n%20a%20Digizen." target="_blank" rel="noopener noreferrer">Consultar con el equipo por WhatsApp</a></dialog>
<dialog id="ada-dialog" aria-labelledby="ada-title"><button class="close" type="button" data-close aria-label="Cerrar solicitud de ADA">×</button><p class="kicker">CONÓCELA TÚ PRIMERO</p><h2 id="ada-title">Conversa con ADA.</h2><p>Datos de mamá, papá o tutor.</p><form id="ada-form"><label for="parent-name">Tu nombre</label><input id="parent-name" name="name" autocomplete="given-name" required maxlength="100"><label for="parent-email">Tu correo</label><input id="parent-email" name="email" type="email" autocomplete="email" required maxlength="254"><label for="parent-phone">Tu WhatsApp <span class="optional">(opcional)</span></label><input id="parent-phone" name="phone" type="tel" autocomplete="tel" maxlength="25"><label for="stage">¿En qué etapa está tu hijo?</label><select id="stage" name="stage" required><option value="">Elige una opción</option><option>Últimos años de primaria</option><option>Secundaria</option><option>Preparatoria</option></select><p class="review-note">Versión de revisión: este formulario aún no envía datos ni accesos a ADA.</p><button class="button primary" type="submit">Solicitar acceso a ADA ↗</button><p id="ada-status" class="form-status" role="status"></p></form><a class="support" href="https://wa.me/522218481116?text=Hola%2C%20quiero%20conocer%20a%20ADA%20antes%20de%20inscribir%20a%20mi%20hijo." target="_blank" rel="noopener noreferrer">Solicitar información al equipo por WhatsApp</a></dialog>
<dialog id="rules-dialog" aria-labelledby="rules-title"><button class="close" type="button" data-close aria-label="Cerrar reglas de ADA">×</button><p class="kicker">ANTES DE EMPEZAR</p><h2 id="rules-title">Las reglas de ADA.</h2><p>Su propósito es educativo. ADA ayuda a pensar y a tomar decisiones; no sustituye a la familia ni a un profesional de la salud.</p><p>La familia recibe avances y resúmenes, no una copia de todo lo que conversa el hijo. La privacidad tiene excepciones cuando una situación requiere ayuda de un adulto.</p><p class="review-note">La liga al documento completo de reglas todavía está pendiente en esta versión de revisión.</p><a class="support" href="mailto:info@gnius.club?subject=Quiero%20conocer%20las%20reglas%20de%20ADA">Pedir el documento al equipo</a></dialog>'''
Path('dist/index.html').write_text(head+header+'<main id="historia">'+'\n'.join(output)+'</main>'+footer+modals+'<script src="config.js"></script><script src="site.js" defer></script></body></html>')
Path('editorial-notes.json').write_text(json.dumps({'source':'digizen-copy-narrativa-ab.md','language_adjustments':replacements,'fact_check':'El dato 72% es de adolescentes de Estados Unidos de 13–17 años, encuesta Common Sense Media 2025, alguna vez. Se precisa el alcance; no se reproduce el tercer lugar de México sin fuente primaria. Se retiran exclusividades no demostradas y la cita textual no verificada de Policía Cibernética.','connections_pending':['pago contado','pago mensualidades','entrega de demo ADA','documento completo de reglas','destino de métricas'],'preserved':'Copy del 20 de septiembre; 13 bloques; nueve viñetas; señales animadas de lectura; mamá y papá presentes; transiciones ADA y cierre compactas; oferta y CTA conservados.'},ensure_ascii=False,indent=2))
print('Created complete variant with',len(output),'sections.')
