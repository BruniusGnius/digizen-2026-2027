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

type DeliveryChannel = 'correo' | 'whatsapp';

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
  protected readonly channel = signal<DeliveryChannel>('correo');
  protected readonly expandedReadMore = signal<ReadonlySet<string>>(new Set());
  protected readonly progress = signal(0);
  protected readonly navScrolled = signal(false);
  protected readonly navWidth = signal<string | null>(null);
  protected readonly navReveal = signal('0');
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

  private frame = 0;
  private clockVideoFrame = 0;
  private observer?: IntersectionObserver;
  private clockVideoTrigger?: ScrollTrigger;
  private clockVideoQuery?: MediaQueryList;
  private chatTrigger?: ScrollTrigger;
  private adaImages: HTMLImageElement[] = [];
  private adaWarmupObserver?: IntersectionObserver;
  private anchorTween?: gsap.core.Tween;
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
    this.handleScroll();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.measureNav);
    window.removeEventListener('load', this.measureNav);
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
  }

  protected toggleTheme(): void {
    this.theme.toggle();
  }
  protected setChannel(channel: DeliveryChannel): void {
    this.channel.set(channel);
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
        // Stay in px instead of switching to 'auto': that layout-mode change
        // can resolve to a fractionally different height than scrollHeight
        // and cause a last-instant micro-jump.
        panel.style.height = opening ? `${inner.scrollHeight}px` : '0px';
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

  protected checkout(plan?: 'diferido' | 'contado'): void {
    if (!plan) {
      const precio = document.querySelector<HTMLElement>('#precio');
      if (precio) this.scrollToElement(precio, 108);
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
    const OFFSET = 108; // igual que el scroll-margin-top de las secciones

    document.addEventListener('click', (event) => {
      const link = (event.target as HTMLElement | null)?.closest?.('a[href^="#"]');
      if (!(link instanceof HTMLAnchorElement)) return;
      const id = link.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector<HTMLElement>(id);
      if (!target) return;

      event.preventDefault();
      this.scrollToElement(target, OFFSET);
      history.pushState(null, '', id);
    });
  }

  private scrollToElement(target: HTMLElement, offset: number): void {
    const soft = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const to = Math.max(0, target.getBoundingClientRect().top + window.scrollY - offset);
    const from = window.scrollY;
    const distance = Math.abs(to - from);
    if (distance < 2) return;

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
    });
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
