// Three-row half-block lettering follows OpenCode's stock logo proportions.
// Its stock logo is split into two color groups; so is ENCOM | CODE.
const glyphs: Record<string, string[]> = {
  E: ['█▀▀▀', '█▀▀ ', '▀▀▀▀'],
  N: ['█▄  █', '██▄ █', '▀ ▀▄▀'],
  C: ['█▀▀▀', '█   ', '▀▀▀▀'],
  O: ['█▀▀█', '█  █', '▀▀▀▀'],
  M: ['█▄ ▄█', '██▀██', '▀   ▀'],
  D: ['█▀▀▄', '█  █', '▀▀▀▀'],
};

export function wordmark(text: string): string[] {
  const letters = [...text].map(letter => glyphs[letter]);
  if (letters.some(letter => !letter)) throw Error('Unsupported logo letter');
  return [0, 1, 2].map(row => letters.map(letter => letter[row]).join(' '));
}

export function banner(width: number, height: number): { content: string; color: string }[] {
  if (height < 12 || width < 27) return [{ content: 'EncomCode', color: '#D8E1DD' }];
  const left = wordmark('ENCOM');
  const right = wordmark('CODE');
  const blue = '#6FC3DF';
  const cyan = '#00EEEE';
  if (width >= left[0].length + right[0].length + 3) {
    return left.map((line, index) => ({ content: line + '  ' + right[index], color: index === 1 ? cyan : blue }));
  }
  return [
    ...left.map(content => ({ content, color: blue })),
    ...right.map(content => ({ content, color: cyan })),
  ];
}
