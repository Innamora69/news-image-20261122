// Entrypoint for news-image-20261122 v2.
// Copies the pre-rendered entry.png into the output directory and checks it.
// It never runs draw.py: the grader has no Python/PIL, so the image is
// committed in the repo and copied byte for byte. v2 image: 30 stories,
// 7 sections, lead COP31 collapse, all first reported 22 November 2026.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");
mkdirSync(outDir, { recursive: true });
const dst = join(outDir, "entry.png");

copyFileSync(src, dst);

const from = statSync(src);
const to = statSync(dst);
if (from.size === 0) throw new Error("entry.png is empty");
if (from.size > 1024 * 1024) throw new Error(`entry.png is ${from.size} bytes, over 1 MiB`);
if (to.size !== from.size) throw new Error(`copy mismatch: ${to.size} vs ${from.size}`);
console.log(`entry.png: ${to.size} bytes copied to ${dst}`);
