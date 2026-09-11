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
import { LucideHand, LucideHeartCrack } from '@lucide/angular';
import { ThemeService } from './core/theme.service';

type DeliveryChannel = 'correo' | 'whatsapp';

@Component({
  selector: 'app-root',
  imports: [LucideHand, LucideHeartCrack],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements AfterViewInit, OnDestroy {
  @ViewChild('adaDialog') private adaDialog?: ElementRef<HTMLDialogElement>;
  protected readonly theme = inject(ThemeService);
  protected readonly channel = signal<DeliveryChannel>('correo');
  protected readonly progress = signal(0);
  protected readonly navScrolled = signal(false);
  protected readonly navWidth = signal<string | null>(null);
  protected readonly navReveal = signal('0');
  private navOpenPx = 0;
  private navClosedPx = 0;
  private navTarget = 0;
  private navCurrent = 0;
  private navFrame = 0;
  private navReady = false;
  protected readonly activeSection = signal('problema');
  protected readonly mobileCtaVisible = signal(false);
  protected readonly mobileCtaClosed = signal(false);
  protected readonly mobileCtaMode = signal<'ada' | 'checkout'>('ada');

  private frame = 0;
  private observer?: IntersectionObserver;
  private trigger?: ScrollTrigger;

  ngAfterViewInit(): void {
    this.setupNarrativeMotion();
    this.setupSectionObserver();
    this.measureNav();
    window.addEventListener('resize', this.measureNav, { passive: true });
    this.handleScroll();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.measureNav);
    cancelAnimationFrame(this.navFrame);
    window.removeEventListener('scroll', this.queueScroll);
    cancelAnimationFrame(this.frame);
    this.observer?.disconnect();
    this.trigger?.kill();
  }

  protected toggleTheme(): void {
    this.theme.toggle();
  }
  protected setChannel(channel: DeliveryChannel): void {
    this.channel.set(channel);
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

  protected checkout(plan: 'mensual' | 'ciclo-msi' | 'contado' = 'ciclo-msi'): void {
    window.dispatchEvent(new CustomEvent('digizen:checkout', { detail: { plan } }));
  }

  // The scroll position sets where the desktop menu should be (62% → 100% width over 280px);
  // a rAF follow loop eases toward it so wheel steps and fast trackpad flicks never snap.
  // Runs in JS on purpose: CSS transitions are cut to 1ms under prefers-reduced-motion.
  private readonly measureNav = (): void => {
    const header = document.querySelector<HTMLElement>('.dg-header');
    if (!header || header.clientWidth === 0) return;
    const style = getComputedStyle(header);
    this.navOpenPx =
      header.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    this.navClosedPx = this.navOpenPx * 0.62;
    this.applyNav(this.navCurrent);
  };

  private updateNav(scrollTop: number): void {
    const t = Math.min(1, Math.max(0, scrollTop / 280));
    this.navTarget = t * t * (3 - 2 * t);
    if (!this.navReady) {
      this.navReady = true;
      this.navCurrent = this.navTarget;
      this.applyNav(this.navCurrent);
      return;
    }
    if (!this.navFrame) this.navFrame = requestAnimationFrame(this.stepNav);
  }

  private readonly stepNav = (): void => {
    const delta = this.navTarget - this.navCurrent;
    this.navCurrent = Math.abs(delta) < 0.001 ? this.navTarget : this.navCurrent + delta * 0.14;
    this.applyNav(this.navCurrent);
    this.navFrame =
      this.navCurrent === this.navTarget ? 0 : requestAnimationFrame(this.stepNav);
  };

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

  private setupNarrativeMotion(): void {
    if (
      typeof window.matchMedia !== 'function' ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    )
      return;
    const visual = document.querySelector<HTMLElement>('[data-criteria-visual]');
    if (!visual) return;
    gsap.registerPlugin(ScrollTrigger);
    const orbit = visual.querySelectorAll('.dg-orbit');
    const labels = visual.querySelectorAll('.dg-feed-labels span');
    const node = visual.querySelector('.dg-criteria-node');
    const timeline = gsap.timeline({ paused: true });
    timeline
      .fromTo(
        labels,
        { opacity: 0.25, x: -12 },
        { opacity: 1, x: 0, stagger: 0.12, duration: 0.5, ease: 'power2.out' },
      )
      .fromTo(
        orbit,
        { scale: 0.82, opacity: 0.2 },
        { scale: 1, opacity: 1, stagger: 0.1, duration: 0.7, ease: 'power3.out' },
        '<.1',
      )
      .fromTo(
        node,
        { scale: 0.9, opacity: 0.5 },
        { scale: 1, opacity: 1, duration: 0.55, ease: 'power2.out' },
        '-=.35',
      );
    this.trigger = ScrollTrigger.create({
      trigger: visual,
      start: 'top 72%',
      once: true,
      onEnter: () => timeline.play(),
    });
  }
}
