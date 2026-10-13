import type { ExtensionAPI } from '@oh-my-pi/pi-coding-agent';
import { center, PI_LOGO } from './art';

export default function (pi: ExtensionAPI) {
  pi.on('session_start', async (_event, ctx) => {
    if (!ctx.hasUI) return;
    ctx.ui.setWidget('encom-omp-startup', (_tui, theme) => ({
      render(width: number) {
        if (width < 18) return [theme.fg('accent', 'Encom OMP')];
        const box = Math.min(width, 36);
        const inner = box - 2;
        const h = '─';
        const border = (s: string) => theme.fg('border', s);
        const row = (content: string) => border('│') + content + border('│');
        const title = ' Encom OMP ';
        const top = border('╭' + h.repeat(3)) + theme.fg('accent', title)
          + border(h.repeat(inner - 3 - title.length) + '╮');
        return [
          top,
          row(' '.repeat(inner)),
          row(theme.fg('text', center('Welcome back!', inner))),
          row(' '.repeat(inner)),
          ...PI_LOGO.map(line => row(theme.fg('borderAccent', center(line, inner)))),
          row(' '.repeat(inner)),
          row(theme.fg('text', center('Encom OMP', inner))),
          row(theme.fg('warning', center('·', inner))),
          border('╰' + h.repeat(inner) + '╯'),
        ];
      },
      invalidate() {},
    }));
  });
  // Display only; the widget leaves the transcript and model context untouched.
  pi.on('before_agent_start', async (_event, ctx) => {
    if (ctx.hasUI) ctx.ui.setWidget('encom-omp-startup', undefined);
  });
}
