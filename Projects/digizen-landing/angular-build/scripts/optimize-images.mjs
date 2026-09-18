import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';

const root = process.cwd();

const pngAssets = [
  'assets/digizen/generated/scenes/dg-scene-a01-hero-phone-hypocrisy-mobile.png',
  'assets/digizen/generated/scenes/dg-scene-a01-hero-phone-hypocrisy.png',
  'assets/digizen/generated/scenes/dg-scene-a02-parent-phone-attachment-mobile.png',
  'assets/digizen/generated/scenes/dg-scene-a02-parent-phone-attachment.png',
  'assets/digizen/generated/scenes/dg-scene-a03-mother-son-dinner-mobile.png',
  'assets/digizen/generated/scenes/dg-scene-a03-mother-son-dinner.png',
  'assets/digizen/generated/scenes/dg-scene-cta-father-son-team-1-1.png',
  'assets/digizen/generated/scenes/dg-scene-a04-clock-scroll-poster.png',
  'assets/digizen/generated/scenes/dg-scene-a04-clock-scroll-4-3.png',
  'assets/digizen/generated/scenes/dg-scene-a05-decision-tree.png',
  'assets/digizen/generated/scenes/dg-scene-a05-decision-tree-16-9.png',
  'assets/digizen/ada-profile-low.png',
  'assets/digizen/digizen-preset-avatar-set-mx-v03-white-03.png',
  'assets/digizen/generated/scenes/dg-scene-a06-trust-father-daughter-mobile.png',
  'assets/digizen/generated/scenes/dg-scene-a06-trust-father-daughter.png',
  'assets/digizen/generated/scenes/dg-scene-a05-father-tests-ada-mobile.png',
  'assets/digizen/generated/scenes/dg-scene-a05-father-tests-ada.png',
  'assets/digizen/generated/scenes/dg-scene-a07-presence-mother-son-mobile.png',
  'assets/digizen/generated/scenes/dg-scene-a07-presence-mother-son.png',
  'assets/digizen/generated/scenes/dg-scene-a08-founder-high-five.png',
  'assets/digizen/generated/scenes/dg-scene-cta-mother-daughter-laptop-1-1.png',
];

function publicPath(assetPath) {
  return join(root, 'public', assetPath);
}

function toWebpPath(assetPath) {
  return publicPath(assetPath.replace(/\.png$/i, '.webp'));
}

function size(path) {
  return existsSync(path) ? statSync(path).size : 0;
}

function pretty(bytes) {
  if (bytes > 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
  if (bytes > 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${bytes} B`;
}

for (const asset of pngAssets) {
  const input = publicPath(asset);
  const output = toWebpPath(asset);
  if (!existsSync(input)) throw new Error(`Missing source image: ${asset}`);
  mkdirSync(dirname(output), { recursive: true });
  execFileSync('cwebp', ['-quiet', '-m', '6', '-q', '82', '-alpha_q', '90', input, '-o', output], {
    stdio: 'inherit',
  });
  console.log(`${asset} -> ${asset.replace(/\.png$/i, '.webp')} (${pretty(size(input))} -> ${pretty(size(output))})`);
}

const seoDir = publicPath('assets/digizen/seo');
const ogDir = publicPath('assets/og');
mkdirSync(seoDir, { recursive: true });
mkdirSync(ogDir, { recursive: true });
const ogpSource = publicPath('assets/digizen/generated/scenes/dg-scene-a01-hero-phone-hypocrisy-mobile.png');
const ogpOutput = join(seoDir, 'digizen-ogp-1200x630.jpg');
const namedOgpOutput = join(ogDir, 'digizen-og-control-caduca-criterio-no.jpg');
execFileSync('magick', [
  ogpSource,
  '-auto-orient',
  '-resize',
  '1200x630^',
  '-gravity',
  'center',
  '-extent',
  '1200x630',
  '-strip',
  '-quality',
  '82',
  ogpOutput,
]);
execFileSync('magick', [ogpOutput, namedOgpOutput]);
console.log(`OGP -> assets/digizen/seo/digizen-ogp-1200x630.jpg (${pretty(size(ogpOutput))})`);
console.log(`OGP -> assets/og/digizen-og-control-caduca-criterio-no.jpg (${pretty(size(namedOgpOutput))})`);
