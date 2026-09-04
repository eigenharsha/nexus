import { compile } from '@mdx-js/mdx';
import { readFileSync } from 'fs';
const files = process.argv.slice(2);
for (const f of files) {
  const src = readFileSync(f, 'utf8').replace(/^---[\s\S]*?---\n/, '');
  try { await compile(src, { format: 'mdx' }); console.log('OK  ', f); }
  catch (e) { console.log('FAIL', f, '->', e.message, e.line ? `(line ${e.line}:${e.column})` : (e.place ? `(line ${e.place.line}:${e.place.column})` : '')); }
}

// Usage:  npm i @mdx-js/mdx@3  (once, anywhere) then:
//   node tools/mdxcheck.mjs curriculum/p4/week-25/*.mdx
// Catches real MDX compile failures that validate.py's regex checks cannot —
// run it on any page carrying inline SVG before pushing.
