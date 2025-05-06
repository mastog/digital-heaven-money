// src/pages/api/upload-md.ts
import fs from 'fs';
import path from 'path';

export async function POST({ request }) {
  const data = await request.json();

  const {
    title, pubDate, author, authImage,
    image, tags, slug, summary, type, content
  } = data;

  const fileName = `${slug}.md`;
  const filePath = path.join(process.cwd(), 'src/content/blog', fileName);

  const frontmatter = `---
title: "${title}"
pubDate: ${pubDate}
author: "${author}"
authImage: "${authImage}"
image: "${image}"
tags: [${tags.split(',').map(tag => `'${tag.trim()}'`).join(', ')}]
slug: ${slug}
summary: "${summary}"
type: "${type}"
---`;

  const fullContent = `${frontmatter}\n\n${content}`;

  try {
    fs.writeFileSync(filePath, fullContent, 'utf-8');
    return new Response(JSON.stringify({ success: true }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
