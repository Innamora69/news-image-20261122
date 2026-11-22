// news-image-20261122 — entrypoint.
// Copies the front-page image this repository holds to the grader's output
// directory. Node 22, standard library only, no network, deterministic:
// every run writes the same bytes.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

const src = new URL('./entry.png', import.meta.url);
const dst = join(outDir, 'entry.png');
copyFileSync(src, dst);

// Both runs must write the same bytes: the copy is byte-identical to the
// committed image by construction, so verify the sizes agree.
const srcBytes = statSync(src).size;
const dstBytes = statSync(dst).size;
if (srcBytes !== dstBytes || dstBytes <= 0 || dstBytes > 1048576) {
  throw new Error(
    `entry.png size mismatch or out of bounds: src=${srcBytes} dst=${dstBytes}`,
  );
}
