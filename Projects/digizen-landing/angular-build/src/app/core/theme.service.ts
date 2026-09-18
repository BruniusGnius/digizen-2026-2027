import { DOCUMENT } from '@angular/common';
import { Injectable, inject, signal } from '@angular/core';

export type Theme = 'light' | 'dark';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly document = inject(DOCUMENT);
  readonly theme = signal<Theme>(this.readTheme());

  toggle(): void {
    this.set(this.theme() === 'light' ? 'dark' : 'light');
  }

  set(theme: Theme): void {
    this.theme.set(theme);
    this.document.documentElement.dataset['theme'] = theme;
    this.document
      .querySelector('meta[name="theme-color"]')
      ?.setAttribute('content', theme === 'dark' ? '#030303' : '#f6f8fb');
    try {
      localStorage.setItem('digizen-theme', theme);
    } catch {
      // The selected theme still works when storage is unavailable.
    }
  }

  private readTheme(): Theme {
    return this.document.documentElement.dataset['theme'] === 'dark' ? 'dark' : 'light';
  }
}
