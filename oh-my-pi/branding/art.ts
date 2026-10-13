// The five rows are Oh-My-Pi's stock PI_LOGO (welcome.ts, installed package).
// Recoloring this mark keeps its familiar block silhouette intact.
export const PI_LOGO = [
  '▀██████████▀',
  ' ╘██    ██  ',
  '  ██    ██  ',
  '  ██    ██  ',
  ' ▄██▄  ▄██▄ ',
] as const;

export function center(text: string, width: number): string {
  const left = Math.max(0, Math.floor((width - text.length) / 2));
  return ' '.repeat(left) + text + ' '.repeat(Math.max(0, width - left - text.length));
}
