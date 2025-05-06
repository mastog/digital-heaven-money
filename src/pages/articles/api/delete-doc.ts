import fs from 'fs';
import path from 'path';

export async function POST({ request }) {
  const { file } = await request.json();
  const filePath = path.join(process.cwd(), 'src/content/blog', file);

  try {
    fs.unlinkSync(filePath);
    return new Response(JSON.stringify({ success: true }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
