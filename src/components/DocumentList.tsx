import React, { useEffect, useState } from 'react';

export default function DocumentList() {
  const [files, setFiles] = useState<string[]>([]);

  const fetchFiles = async () => {
    const res = await fetch('/articles/api/list-docs');
    const data = await res.json();
    setFiles(data.files);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const deleteFile = async (file: string) => {
    const res = await fetch('/articles/api/delete-doc', {
      method: 'POST',
      body: JSON.stringify({ file }),
      headers: { 'Content-Type': 'application/json' },
    });
    if (res.ok) fetchFiles();
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-xl font-bold mb-4">📄 Existing Documents</h2>
      <ul className="divide-y bg-gray border rounded-xl shadow-xl">
        {files.length === 0 ? (
          <li className="p-4 text-gray-500">No documents found.</li>
        ) : (
          files.map(file => (
            <li key={file} className="p-4 flex justify-between items-center">
              <a
                href={`/articles/${file}`}
                className="truncate max-w-[80%] hover:underline"
              >
                {file}
              </a>
              <button
                onClick={() => deleteFile(file)}
                className="text-red-600 hover:underline"
              >
                Delete
              </button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
