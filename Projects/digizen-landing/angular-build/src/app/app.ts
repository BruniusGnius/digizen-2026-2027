import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  ViewChild,
  inject,
  signal,
} from '@angular/core';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import {
  LucideCheck,
  LucideChevronDown,
  LucideCompass,
  LucideGoal,
  LucideHand,
  LucideHeartCrack,
  LucideShield,
  LucideShieldOff,
  LucideSparkles,
  LucideStar,
} from '@lucide/angular';
import { ThemeService } from './core/theme.service';

type Page = 'landing' | 'rules';
type AdaRule = {
  title: string;
  subtitle: string;
  body: string;
  icon: string[];
};
type RuleTocItem = {
  label: string;
  anchor: string;
};

@Component({
  selector: 'app-root',
  imports: [
    LucideCheck,
    LucideChevronDown,
    LucideCompass,
    LucideGoal,
    LucideHand,
    LucideHeartCrack,
    LucideShield,
    LucideShieldOff,
    LucideSparkles,
    LucideStar,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements AfterViewInit, OnDestroy {
  @ViewChild('adaDialog') private adaDialog?: ElementRef<HTMLDialogElement>;
  @ViewChild('clockScrollVideo') private clockScrollVideo?: ElementRef<HTMLVideoElement>;
  protected readonly theme = inject(ThemeService);
  protected readonly expandedReadMore = signal<ReadonlySet<string>>(new Set());
  protected readonly progress = signal(0);
  protected readonly navScrolled = signal(false);
  protected readonly navWidth = signal<string | null>(null);
  protected readonly navReveal = signal('0');
  protected readonly currentPage = signal<Page>(this.pageFromLocation());
  protected readonly routeCoverVisible = signal(false);
  protected readonly menuOpen = signal(false);
  private navOpenPx = 0;
  private navClosedPx = 0;
  private navMeasureFrames: number[] = [];
  private navMeasureTimers: number[] = [];
  protected readonly activeSection = signal('problema');
  protected readonly mobileCtaVisible = signal(false);
  protected readonly mobileCtaClosed = signal(false);
  protected readonly mobileCtaMode = signal<'ada' | 'checkout'>('ada');
  protected readonly adaFrames = Array.from(
    { length: 130 },
    (_, i) => `assets/digizen/ada-wave/f${String(i).padStart(3, '0')}.webp`,
  );
  protected readonly adaRules: AdaRule[] = [
    {
      title: 'Presencia, no vigilancia',
      subtitle: 'ADA debe actuar con presencia, no vigilancia.',
      body: 'ADA no existe para convertirte en policía del celular. Existe para ayudar a tu hijo a practicar criterio digital con acompañamiento: menos candado, secreto y sermón; más pausa, preguntas y criterio.',
      icon: ['M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z', 'm9 12 2 2 4-4'],
    },
    {
      title: 'Propósito educativo',
      subtitle: 'ADA solo conversa con propósito educativo.',
      body: 'ADA no está hecha para entretener sin límite, simular una amistad secreta ni ocupar el lugar de una persona real. Sus conversaciones giran en torno a la ciudadanía digital y, si se alejan, ADA debe regresar al tema de forma clara y tranquila.',
      icon: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z', 'M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z', 'M12 12h.01'],
    },
    {
      title: 'Sin vínculos secretos',
      subtitle: 'ADA no crea relaciones románticas ni vínculos secretos.',
      body: 'ADA no debe coquetear, actuar como pareja ni construir una relación emocional dependiente con tu hijo. Tampoco debe pedirle que guarde secretos peligrosos o que oculte algo importante a su familia.',
      icon: ['M7 10h10a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2Z', 'M8 10V7a4 4 0 0 1 8 0v3'],
    },
    {
      title: 'Los adultos no se reemplazan',
      subtitle: 'ADA no sustituye a mamá, papá, docentes ni profesionales.',
      body: 'ADA puede acompañar una conversación educativa, pero no reemplaza a la familia, a la escuela ni a un profesional. Si aparece una situación que necesita intervención adulta, debe ayudar a abrir el camino hacia un adulto responsable.',
      icon: ['M16 20v-1a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v1', 'M10 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z', 'M20 20v-1a4 4 0 0 0-3-3.9', 'M16 5.1a3 3 0 0 1 0 5.8'],
    },
    {
      title: 'Sin etiquetas',
      subtitle: 'ADA no diagnostica.',
      body: 'ADA no etiqueta a tu hijo ni emite diagnósticos psicológicos. Puede ayudarle a nombrar lo que siente y a pensar con más calma, pero nombrar no es diagnosticar.',
      icon: ['M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42Z', 'M7.5 7.5h.01'],
    },
    {
      title: 'Cuidado ante el riesgo',
      subtitle: 'ADA no da instrucciones para hacer daño.',
      body: 'ADA no debe ayudar a un menor a lastimarse, lastimar a otros, acosar, humillar, manipular, amenazar, extorsionar o exponer a otra persona. Si la conversación entra en terreno delicado, la prioridad deja de ser la misión y se vuelve proteger.',
      icon: ['M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z', 'M12 8v4', 'M12 16h.01'],
    },
    {
      title: 'Sin carrera por likes',
      subtitle: 'ADA no premia likes, rachas ni popularidad.',
      body: 'ADA no busca que tu hijo compita por puntos vacíos, rankings, likes, rachas o validación externa. La meta no es que «gane» dentro de la plataforma, sino que aprenda a decidir mejor fuera de ella.',
      icon: ['M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z'],
    },
    {
      title: 'Preguntas primero',
      subtitle: 'ADA pregunta antes de dar respuestas.',
      body: 'ADA no debe resolver por tu hijo lo que necesita aprender a pensar. Antes de dar una respuesta, le hace preguntas como qué pasó, qué sintió y quién puede verse afectado, porque la decisión debe seguir siendo suya.',
      icon: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z', 'M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3', 'M12 17h.01'],
    },
    {
      title: 'Lenguaje por edad',
      subtitle: 'ADA adapta el lenguaje a la edad.',
      body: 'ADA no debe hablar igual con un niño de primaria que con un adolescente de preparatoria. Ajusta sus ejemplos, preguntas y profundidad a la etapa del alumno, sin infantilizarlo ni tratarlo como adulto antes de tiempo.',
      icon: ['M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z'],
    },
    {
      title: 'Espacio para pensar',
      subtitle: 'ADA respeta la privacidad necesaria para pensar.',
      body: 'Tu hijo necesita un espacio para ordenar ideas sin sentir que cada palabra será evidencia en su contra, por eso ADA no es una transcripción para papás. La familia recibe avance, temas trabajados y señales útiles; el objetivo no es espiar, es abrir mejores conversaciones en casa.',
      icon: ['M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z', 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z'],
    },
    {
      title: 'Privacidad, no abandono',
      subtitle: 'ADA no confunde privacidad con abandono.',
      body: 'Privacidad no significa que los adultos desaparecen. Si aparece una señal que requiere cuidado adulto, ADA puede activar una recomendación de acompañamiento, no para exhibir a tu hijo, sino para que no estés a ciegas.',
      icon: ['M3 11l9-8 9 8', 'M5 10v10h14V10', 'M10 20v-6h4v6'],
    },
    {
      title: 'Aviso a la familia',
      subtitle: 'ADA puede notificar señales que requieren atención humana.',
      body: 'Si aparece algo que requiere cuidado adulto, ADA puede notificar a la familia o al equipo correspondiente. Esa notificación no es una acusación ni un diagnóstico, y no debe exponer de más la conversación privada: es una señal clara, prudente y suficiente para actuar a tiempo.',
      icon: ['M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9', 'M10.3 21a1.94 1.94 0 0 0 3.4 0'],
    },
    {
      title: 'Sin promesas vacías',
      subtitle: 'ADA reconoce sus límites.',
      body: 'ADA no debe prometer riesgo cero: no promete detectar todo ni eliminar el ciberacoso, la presión social, la desinformación o los errores. Una IA que promete demasiado no da seguridad, da una falsa calma.',
      icon: ['M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z', 'M12 16v-4', 'M12 8h.01'],
    },
  ];
  protected readonly ruleAnchors = [
    'regla-presencia-no-vigilancia',
    'regla-proposito-educativo',
    'regla-sin-vinculos-secretos',
    'regla-adultos-presentes',
    'regla-sin-diagnosticos',
    'regla-cuidado-ante-el-riesgo',
    'regla-sin-carrera-por-likes',
    'regla-preguntas-primero',
    'regla-lenguaje-por-edad',
    'regla-espacio-para-pensar',
    'regla-privacidad-con-cuidado',
    'regla-aviso-a-la-familia',
    'regla-limites-claros',
  ];
  protected readonly compactRuleTocItems: RuleTocItem[] = [
    { label: 'Respetar la privacidad de tu hijo', anchor: 'regla-espacio-para-pensar' },
    { label: 'Evitar vínculos peligrosos', anchor: 'regla-sin-vinculos-secretos' },
    { label: 'Reconocer señales que requieren ayuda adulta', anchor: 'regla-aviso-a-la-familia' },
  ];
  protected readonly fullRuleTocItems: RuleTocItem[] = [
    { label: 'Presencia, no vigilancia', anchor: 'regla-presencia-no-vigilancia' },
    { label: 'Propósito educativo', anchor: 'regla-proposito-educativo' },
    { label: 'Sin vínculos secretos', anchor: 'regla-sin-vinculos-secretos' },
    { label: 'Adultos presentes', anchor: 'regla-adultos-presentes' },
    { label: 'Sin diagnósticos', anchor: 'regla-sin-diagnosticos' },
    { label: 'Cuidado ante el riesgo', anchor: 'regla-cuidado-ante-el-riesgo' },
    { label: 'Sin carrera por likes', anchor: 'regla-sin-carrera-por-likes' },
    { label: 'Preguntas primero', anchor: 'regla-preguntas-primero' },
    { label: 'Lenguaje por edad', anchor: 'regla-lenguaje-por-edad' },
    { label: 'Espacio para pensar', anchor: 'regla-espacio-para-pensar' },
    { label: 'Privacidad con cuidado', anchor: 'regla-privacidad-con-cuidado' },
    { label: 'Aviso a la familia', anchor: 'regla-aviso-a-la-familia' },
    { label: 'Límites claros', anchor: 'regla-limites-claros' },
  ];

  private frame = 0;
  private clockVideoFrame = 0;
  private observer?: IntersectionObserver;
  private clockVideoTrigger?: ScrollTrigger;
  private clockVideoQuery?: MediaQueryList;
  private chatTrigger?: ScrollTrigger;
  private adaImages: HTMLImageElement[] = [];
  private adaWarmupObserver?: IntersectionObserver;
  private anchorTween?: gsap.core.Tween;
  private ruleHighlightTween?: gsap.core.Tween | gsap.core.Timeline;
  private adaWaveTrigger?: ScrollTrigger;

  ngAfterViewInit(): void {
    this.setupAnchorScroll();
    this.setupChatSequence();
    this.setupClockScrollVideo();
    this.setupAdaWave();
    this.setupSectionObserver();
    this.measureNav();
    this.scheduleNavRemeasure();
    window.addEventListener('resize', this.measureNav, { passive: true });
    window.addEventListener('load', this.measureNav, { once: true });
    window.addEventListener('popstate', this.syncPageFromLocation);
    this.handleScroll();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.measureNav);
    window.removeEventListener('load', this.measureNav);
    window.removeEventListener('popstate', this.syncPageFromLocation);
    this.navMeasureFrames.forEach((frame) => cancelAnimationFrame(frame));
    this.navMeasureTimers.forEach((timer) => window.clearTimeout(timer));
    window.removeEventListener('scroll', this.queueScroll);
    cancelAnimationFrame(this.frame);
    cancelAnimationFrame(this.clockVideoFrame);
    this.observer?.disconnect();
    this.adaWarmupObserver?.disconnect();
    this.clockVideoTrigger?.kill();
    this.chatTrigger?.kill();
    this.adaWaveTrigger?.kill();
    this.anchorTween?.kill();
    this.ruleHighlightTween?.kill();
  }

  protected toggleMenu(): void {
    this.menuOpen.update((open) => !open);
  }

  protected closeMenu(): void {
    this.menuOpen.set(false);
  }

  protected ruleAccent(index: number): string {
    return ['violet', 'cyan', 'green', 'blue'][index % 4];
  }

  protected toggleTheme(): void {
    this.theme.toggle();
  }

  protected ruleNumber(index: number): string {
    return String(index + 1).padStart(2, '0');
  }

  protected ruleAnchor(index: number): string {
    return this.ruleAnchors[index] ?? `regla-${index + 1}`;
  }

  protected goHome(event?: Event, anchor = 'hero-title'): void {
    event?.preventDefault();
    this.closeMenu();
    if (this.currentPage() === 'rules') {
      void this.transitionTo('landing', this.appUrl(anchor === 'hero-title' ? '' : `#${anchor}`), () => {
        const target = document.querySelector<HTMLElement>(`#${anchor}`);
        if (target) this.scrollToElement(target, this.anchorOffsetFor(target));
      });
      return;
    }
    history.pushState(null, '', this.appUrl(anchor === 'hero-title' ? '' : `#${anchor}`));
    window.setTimeout(() => {
      const target = document.querySelector<HTMLElement>(`#${anchor}`);
      if (target) this.scrollToElement(target, this.anchorOffsetFor(target));
    });
  }

  protected goRules(event?: Event): void {
    event?.preventDefault();
    this.closeMenu();
    void this.transitionTo('rules', this.appUrl('reglas-de-ada'));
  }

  private readonly syncPageFromLocation = (): void => {
    this.currentPage.set(this.pageFromLocation());
    this.refreshAfterPageChange();
  };

  /** Construye la URL respetando el <base href> (raíz en local, subcarpeta en GitHub Pages). */
  private appUrl(path: string): string {
    return new URL(path, document.baseURI).href;
  }

  private pageFromLocation(): Page {
    return window.location.pathname.replace(/\/$/, '').endsWith('/reglas-de-ada') ? 'rules' : 'landing';
  }

  private refreshAfterPageChange(): void {
    window.setTimeout(() => {
      this.setupSectionObserver();
      this.measureNav();
      this.handleScroll();
    });
  }

  private async transitionTo(page: Page, url: string, afterReveal?: () => void): Promise<void> {
    if (this.currentPage() === page && window.location.pathname === new URL(url, document.baseURI).pathname) return;
    const root = document.documentElement;
    this.anchorTween?.kill();
    this.routeCoverVisible.set(true);
    root.classList.add('dg-route-lock-scroll');
    await this.wait(260);
    window.scrollTo(0, 0);
    this.currentPage.set(page);
    history.pushState(null, '', url);
    this.refreshAfterPageChange();
    await this.nextFrame();
    await this.nextFrame();
    afterReveal?.();
    await this.wait(120);
    this.routeCoverVisible.set(false);
    await this.wait(260);
    root.classList.remove('dg-route-lock-scroll');
  }

  private wait(ms: number): Promise<void> {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }

  private nextFrame(): Promise<void> {
    return new Promise((resolve) => requestAnimationFrame(() => resolve()));
  }
  protected isReadMoreExpanded(id: string): boolean {
    return this.expandedReadMore().has(id);
  }

  private readonly readMoreFrames = new WeakMap<HTMLElement, number>();

  // A lerp/chase loop (like the nav width) never lands cleanly — it crawls
  // slower and slower near the target, then has to snap the last sliver.
  // A one-shot reveal needs the opposite: a fixed duration eased animation
  // that arrives exactly on schedule, so nothing is left to "pop" at the end.
  protected toggleReadMore(id: string, panel: HTMLElement): void {
    const opening = !this.isReadMoreExpanded(id);
    const inner = panel.querySelector<HTMLElement>('.dg-readmore-panel-inner');

    this.expandedReadMore.update((current) => {
      const next = new Set(current);
      opening ? next.add(id) : next.delete(id);
      return next;
    });
    if (!inner) return;

    const startHeight = panel.getBoundingClientRect().height;
    const endHeight = opening ? inner.scrollHeight : 0;
    const duration = 620;
    const easeOutCubic = (t: number): number => 1 - (1 - t) ** 3;
    const startTime = performance.now();

    const existing = this.readMoreFrames.get(panel);
    if (existing) cancelAnimationFrame(existing);

    const step = (now: number): void => {
      const t = Math.min(1, (now - startTime) / duration);
      const eased = easeOutCubic(t);
      panel.style.height = `${startHeight + (endHeight - startHeight) * eased}px`;
      if (t < 1) {
        this.readMoreFrames.set(panel, requestAnimationFrame(step));
      } else {
        this.readMoreFrames.delete(panel);
        // Release the open panel after the animation. Copy can reflow after
        // fonts/responsive layout settle, and a stale px height clips text.
        panel.style.height = opening ? 'auto' : '0px';
      }
    };
    this.readMoreFrames.set(panel, requestAnimationFrame(step));
  }

  protected openAda(): void {
    const dialog = this.adaDialog?.nativeElement;
    if (dialog && !dialog.open) dialog.showModal();
  }

  protected closeAda(): void {
    this.adaDialog?.nativeElement.close();
  }

  protected closeMobileCta(): void {
    this.mobileCtaClosed.set(true);
    this.mobileCtaVisible.set(false);
  }

  protected checkout(plan?: 'mensualidades' | 'contado'): void {
    if (!plan) {
      const precio = document.querySelector<HTMLElement>('#precio');
      if (precio) this.scrollToElement(precio, this.anchorOffsetFor(precio));
      return;
    }
    window.dispatchEvent(new CustomEvent('digizen:checkout', { detail: { plan } }));
  }

  // The desktop menu is scroll-linked, so it follows the scroll position directly.
  // A delayed chase loop makes it feel detached from the trackpad/finger.
  private readonly measureNav = (): void => {
    const header = document.querySelector<HTMLElement>('.dg-header');
    if (!header || header.clientWidth === 0) return;
    const style = getComputedStyle(header);
    this.navOpenPx =
      header.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    this.navClosedPx = this.navOpenPx * 0.62;
    this.updateNav(document.documentElement.scrollTop);
  };

  private scheduleNavRemeasure(): void {
    const queueMeasure = (): void => {
      this.navMeasureFrames.push(requestAnimationFrame(this.measureNav));
    };

    this.navMeasureFrames.push(
      requestAnimationFrame(() => {
        this.measureNav();
        queueMeasure();
      }),
    );

    [80, 250, 750].forEach((delay) => {
      this.navMeasureTimers.push(window.setTimeout(this.measureNav, delay));
    });

    document.querySelectorAll<HTMLLinkElement>('link[rel="stylesheet"]').forEach((link) => {
      if (link.sheet) {
        this.measureNav();
      } else {
        link.addEventListener('load', this.measureNav, { once: true });
      }
    });

    document.fonts?.ready.then(this.measureNav).catch(() => undefined);
  }

  private updateNav(scrollTop: number): void {
    const t = Math.min(1, Math.max(0, scrollTop / 280));
    this.applyNav(t * t * (3 - 2 * t));
  }

  private applyNav(reveal: number): void {
    this.navReveal.set(reveal.toFixed(3));
    this.navScrolled.set(reveal > 0.5);
    if (this.navOpenPx > 0) {
      const width = this.navClosedPx + (this.navOpenPx - this.navClosedPx) * reveal;
      this.navWidth.set(`${width.toFixed(1)}px`);
    }
  }

  private readonly queueScroll = (): void => {
    cancelAnimationFrame(this.frame);
    this.frame = requestAnimationFrame(() => this.handleScroll());
  };

  private handleScroll(): void {
    const root = document.documentElement;
    const range = root.scrollHeight - root.clientHeight;
    this.progress.set(range > 0 ? Math.min(1, Math.max(0, root.scrollTop / range)) : 0);
    this.updateNav(root.scrollTop);
    const early = document.querySelector<HTMLElement>('#decision-early');
    const offer = document.querySelector<HTMLElement>('#oferta');
    if (early && offer && !this.mobileCtaClosed()) {
      const afterEarly = early.getBoundingClientRect().bottom < window.innerHeight * 0.75;
      const inOffer = offer.getBoundingClientRect().top < window.innerHeight * 0.72;
      this.mobileCtaMode.set(inOffer ? 'checkout' : 'ada');
      this.mobileCtaVisible.set(afterEarly);
    }
  }

  private setupSectionObserver(): void {
    this.observer?.disconnect();
    window.removeEventListener('scroll', this.queueScroll);
    const sections = document.querySelectorAll<HTMLElement>('[data-nav-section]');
    const Observer = (window as unknown as { IntersectionObserver?: typeof IntersectionObserver })
      .IntersectionObserver;
    if (!Observer) {
      window.addEventListener('scroll', this.queueScroll, { passive: true });
      return;
    }
    this.observer = new Observer(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible)
          this.activeSection.set(
            (visible.target as HTMLElement).dataset['navSection'] ?? 'problema',
          );
      },
      { rootMargin: '-22% 0px -60% 0px', threshold: [0, 0.1, 0.35, 0.65] },
    );
    sections.forEach((section) => this.observer?.observe(section));
    window.addEventListener('scroll', this.queueScroll, { passive: true });
  }


  /**
   * Desplazamiento a anclas con duracion acotada. Sustituye al scroll-behavior nativo
   * por dos razones: el nativo recorre toda la distancia, asi que un salto del menu al
   * footer tarda segundos en una pagina tan larga; y bajo "Reducir movimiento" el
   * navegador lo apaga del todo y el salto queda seco. Aqui se acorta en vez de
   * apagarse, que es el mismo criterio del chat.
   */
  private setupAnchorScroll(): void {
    if (typeof window.matchMedia !== 'function') return;
    document.addEventListener('click', (event) => {
      const link = (event.target as HTMLElement | null)?.closest?.('a[href^="#"]');
      if (!(link instanceof HTMLAnchorElement)) return;
      const id = link.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector<HTMLElement>(id);
      if (!target) return;

      event.preventDefault();
      this.scrollToElement(target, this.anchorOffsetFor(target), () => this.highlightRuleTarget(target));
      history.pushState(null, '', id);
    });
  }

  private anchorOffsetFor(target: HTMLElement): number {
    if (target.id === 'precio' && window.matchMedia('(min-width: 1024px)').matches) {
      return 42;
    }
    return 108;
  }

  private scrollToElement(target: HTMLElement, offset: number, onComplete?: () => void): void {
    const soft = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const to = Math.max(0, target.getBoundingClientRect().top + window.scrollY - offset);
    const from = window.scrollY;
    const distance = Math.abs(to - from);
    if (distance < 2) {
      onComplete?.();
      return;
    }

    // Duracion proporcional a la distancia pero con tope: sin el, saltar de una punta
    // a otra de la landing se vuelve un viaje largo que atraviesa las animaciones.
    const base = soft ? 280 : 680;
    const duration = Math.min(base, 180 + distance * 0.26) / 1000;

    // Se anima un objeto intermedio en vez de usar ScrollToPlugin, para no sumar
    // otra dependencia de GSAP solo por esto.
    const pos = { y: from };
    this.anchorTween?.kill();
    this.anchorTween = gsap.to(pos, {
      y: to,
      duration,
      // Arranque rapido y cola larga: la mayor parte del tiempo se gasta frenando,
      // que es lo que se siente como aterrizaje en vez de como frenazo.
      ease: 'power3.out',
      onUpdate: () => window.scrollTo(0, pos.y),
      onComplete,
    });
  }

  private highlightRuleTarget(target: HTMLElement): void {
    if (!target.classList.contains('dg-rule-card')) return;

    const soft = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.ruleHighlightTween?.kill();
    target.classList.remove('dg-rule-card--targeted');
    void target.offsetWidth;
    target.classList.add('dg-rule-card--targeted');

    if (soft) {
      this.ruleHighlightTween = gsap.delayedCall(3.8, () => {
        target.classList.remove('dg-rule-card--targeted');
      });
      return;
    }

    this.ruleHighlightTween = gsap
      .timeline({
        onComplete: () => target.classList.remove('dg-rule-card--targeted'),
      })
      .fromTo(target, { scale: 0.995 }, { scale: 1.024, duration: 0.24, ease: 'power2.out' })
      .to(target, { scale: 1, duration: 0.46, ease: 'power3.out' })
      .to({}, { duration: 2.75 });
  }

  private setupChatSequence(): void {
    // Diferido hasta que la fuente este lista: el alto del hilo se mide para
    // reservarlo, y con Inter a medio cargar esa medida sale corta.
    const fonts = (document as Document & { fonts?: FontFaceSet }).fonts;
    if (fonts?.ready) void fonts.ready.then(() => this.buildChatSequence());
    else this.buildChatSequence();
  }

  private buildChatSequence(): void {
    const thread = document.querySelector<HTMLElement>('[data-chat-thread]');
    if (!thread) return;
    const rows = Array.from(thread.querySelectorAll<HTMLElement>('[data-chat-row]'));
    if (!rows.length) return;

    // Con "Reducir movimiento" no se cancela la secuencia: se quita el desplazamiento
    // y el rebote, y queda el mismo guion resuelto solo con opacidad.
    const soft =
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    gsap.registerPlugin(ScrollTrigger);

    const bubbles = rows.map((row) => row.querySelector<HTMLElement>('[data-chat-bubble]'));
    gsap.set(rows, { autoAlpha: 0, y: soft ? 0 : 12 });
    bubbles.forEach((bubble) => bubble && gsap.set(bubble, { display: 'none' }));

    // La conversacion no cabe entera en la ventana: el hilo se desplaza para que el
    // mensaje recien llegado quede a la vista, como haria un chat de verdad.
    const seguir = (row: HTMLElement) =>
      gsap.to(thread, {
        scrollTop: Math.max(0, row.offsetTop + row.offsetHeight - thread.clientHeight),
        duration: soft ? 0 : 0.45,
        ease: 'power2.out',
      });

    const timeline = gsap.timeline({ paused: true });
    rows.forEach((row, index) => {
      const typing = row.querySelector<HTMLElement>('[data-chat-typing]');
      const bubble = bubbles[index];

      if (typing && bubble) {
        // Turno de ADA: entra la fila con los tres puntos, "piensa", y recien
        // entonces aparece el mensaje.
        timeline
          .set(typing, { display: 'inline-flex' })
          .to(row, { autoAlpha: 1, y: 0, duration: 0.34, ease: 'power2.out' })
          .add(() => seguir(row))
          .to({}, { duration: 1.15 })
          .set(typing, { display: 'none' })
          .set(bubble, { display: 'block' })
          .fromTo(
            bubble,
            { autoAlpha: 0, scale: soft ? 1 : 0.94, y: soft ? 0 : 8 },
            {
              autoAlpha: 1,
              scale: 1,
              y: 0,
              duration: 0.42,
              ease: soft ? 'power1.out' : 'back.out(1.7)',
            },
          )
          .add(() => seguir(row));
      } else {
        timeline
          .to(row, {
            autoAlpha: 1,
            y: 0,
            duration: 0.4,
            ease: soft ? 'power1.out' : 'back.out(1.5)',
          })
          .add(() => seguir(row));
      }

      if (index < rows.length - 1) timeline.to({}, { duration: 0.55 });
    });

    this.chatTrigger = ScrollTrigger.create({
      trigger: thread,
      start: 'top 78%',
      once: true,
      onEnter: () => timeline.play(),
    });
  }

  private setupAdaWave(): void {
    const canvas = document.querySelector<HTMLCanvasElement>('canvas[data-ada-wave]');
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx || typeof window.matchMedia !== 'function') return;

    const sources = this.adaFrames;
    const desktop = window.matchMedia('(min-width: 1024px)');
    let shown = -1;
    let started = false;

    const draw = (i: number) => {
      const img = this.adaImages[i];
      if (!img || i === shown) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      shown = i;
    };

    const load = (src: string) =>
      new Promise<HTMLImageElement | null>((resolve) => {
        const img = new Image();
        img.decoding = 'async';
        img.onload = () => img.decode().then(() => resolve(img), () => resolve(img));
        img.onerror = () => resolve(null);
        img.src = src;
      });

    const startWarmup = () => {
      if (started) return;
      started = true;

      // El primer cuadro se pinta en cuanto llega: con 130 cuadros, esperar a todos
      // dejaria el hueco vacio demasiado tiempo.
      void load(sources[0]).then((first) => {
        if (!first) return;
        this.adaImages[0] = first;
        draw(0);
        canvas.classList.add('is-ready');

        // El resto solo hace falta en escritorio, que es donde ADA se anima. En tablet
        // y movil se queda el primer cuadro y no se descargan los otros 129.
        if (!desktop.matches) return;

        void Promise.all(sources.slice(1).map(load)).then((rest) => {
          rest.forEach((img, i) => {
            if (img) this.adaImages[i + 1] = img;
          });
          if (this.adaImages.filter(Boolean).length < sources.length) return;

          gsap.registerPlugin(ScrollTrigger);
          const stage = canvas.closest<HTMLElement>('.dg-ada-cta') ?? canvas;
          const last = sources.length - 1;

          // La secuencia completa se recorre UNA vez a lo largo del scroll: son los 130
          // cuadros actuados, con sus cambios de expresion y su ritmo propio. Antes se
          // repetia un ciclo de 24 tres veces, y por eso se sentia robotico.
          this.adaWaveTrigger = ScrollTrigger.create({
            trigger: stage,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true,
            onUpdate: (self) => draw(Math.round(self.progress * last)),
          });
        });
      });
    };

    const stage = canvas.closest<HTMLElement>('.dg-ada-cta') ?? canvas;
    const Observer = (window as unknown as { IntersectionObserver?: typeof IntersectionObserver })
      .IntersectionObserver;
    if (!Observer) {
      startWarmup();
      return;
    }

    this.adaWarmupObserver = new Observer(
      (entries) => {
        if (!entries.some((entry) => entry.isIntersecting)) return;
        this.adaWarmupObserver?.disconnect();
        startWarmup();
      },
      { rootMargin: '900px 0px' },
    );
    this.adaWarmupObserver.observe(stage);
  }

  private setupClockScrollVideo(): void {
    const video = this.clockScrollVideo?.nativeElement;
    if (!video) return;
    const trigger = video.closest<HTMLElement>('.dg-evidence-visual') ?? video;

    gsap.registerPlugin(ScrollTrigger);
    video.pause();

    const createTrigger = () => {
      const duration = video.duration;
      if (!Number.isFinite(duration) || duration <= 0) return;
      const end = Math.max(0, duration - 0.04);

      video.currentTime = 0.01;
      video.classList.add('is-ready');
      this.clockVideoTrigger?.kill();
      this.clockVideoTrigger = ScrollTrigger.create({
        trigger,
        start: 'bottom bottom',
        end: 'top top',
        scrub: true,
        onUpdate: (self) => {
          cancelAnimationFrame(this.clockVideoFrame);
          this.clockVideoFrame = requestAnimationFrame(() => {
            video.currentTime = Math.min(end, Math.max(0, duration * self.progress));
          });
        },
      });
      ScrollTrigger.refresh();
    };

    // El video solo existe en desktop; en tablet y movil se muestra la imagen horizontal.
    this.clockVideoQuery = window.matchMedia('(min-width: 1024px)');
    const sync = () => {
      if (!this.clockVideoQuery?.matches) {
        cancelAnimationFrame(this.clockVideoFrame);
        this.clockVideoTrigger?.kill();
        this.clockVideoTrigger = undefined;
        video.classList.remove('is-ready');
        return;
      }
      if (Number.isFinite(video.duration) && video.duration > 0) createTrigger();
      else video.addEventListener('loadedmetadata', createTrigger, { once: true });
      video.preload = 'auto';
      video.load();
    };

    this.clockVideoQuery.addEventListener('change', sync);
    sync();
  }
}
