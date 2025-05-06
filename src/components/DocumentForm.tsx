import React, { useState } from 'react';

export default function DocumentForm() {
  const [form, setForm] = useState({
    title: '',
    pubDate: new Date().toISOString().slice(0, 10),
    author: '',
    authImage: '',
    image: '',
    tags: '',
    slug: '',
    summary: '',
    type: 'Article',
    content: '',
  });

  const [showForm, setShowForm] = useState(false); // 控制表单显示/隐藏

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/articles/api/upload-md', {
      method: 'POST',
      body: JSON.stringify(form),
      headers: { 'Content-Type': 'application/json' },
    });

    if (res.ok) {
      const {showNotification} = await import('../utils/notifications.js');
      showNotification(['Document created successfully']);
      setForm(prev => ({ ...prev, title: '', content: '', slug: '' })); // Reset common fields
    } else {
      const {showNotification} = await import('../utils/notifications.js');
      showNotification(['Creation failed']);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">📝 Create New Document</h2>

      {/* 切换表单显示状态的按钮 */}
      <button
        onClick={() => setShowForm(prev => !prev)}
        className="btn-primary mb-4 transition-all duration-300 min-w-[213px]"
      >
        {showForm ? 'Hide Form' : '➕ New Document'}
      </button>

      {/* 丝滑展开动画容器 */}
      <div
        className={`transition-all duration-500 ease-in-out overflow-hidden ${
          showForm
            ? 'max-h-[1263px] opacity-100 scale-100'
            : 'max-h-0 opacity-0 scale-95'
        }`}
      >
        <form
          onSubmit={handleSubmit}
          className="bg-gray shadow-xl border border-black rounded-2xl sm:p-6 h-full w-full"
        >
          {[
            { name: 'title', type: 'text', required: true },
            { name: 'pubDate', type: 'date', required: true },
            { name: 'author', type: 'text', required: true },
            { name: 'authImage', type: 'text', placeholder: 'Fill in the picture network link' },
            { name: 'image', type: 'text', placeholder: 'Fill in the picture network link' },
            { name: 'tags', type: 'text', placeholder: 'Comma-separated' },
            { name: 'slug', type: 'text', required: true },
            { name: 'summary', type: 'text' },
            { name: 'type', type: 'text' },
          ].map(({ name, type, required, placeholder }) => (
            <div key={name}>
              <label className="block text-black mb-2 cursor-default">
                {name
                  .replace(/([A-Z])/g, ' $1')
                  .replace(/^./, c => c.toUpperCase())}
              </label>
              <input
                type={type}
                name={name}
                required={required}
                placeholder={placeholder}
                value={(form as any)[name]}
                onChange={handleChange}
                className="w-full px-[30px] py-[18px] border border-black rounded-[14px] text-black outline-none shadow-sm focus:border-darkgray focus:ring-2 focus:ring-darkgray mb-2 hover:border-gray-600 transition-colors"
              />
            </div>
          ))}

          <div>
            <label className="block text-black mb-2 cursor-default">Markdown Content</label>
            <textarea
              name="content"
              rows={8}
              required
              value={form.content}
              onChange={handleChange}
              className="w-full px-[30px] py-[18px] border border-black rounded-[14px] text-black outline-none shadow-sm focus:border-darkgray focus:ring-2 focus:ring-darkgray mb-3"
              placeholder="Write your markdown content here..."
            />
          </div>

          <button type="submit" className="btn-primary">
            Create Document
          </button>
        </form>
      </div>
    </div>
  );
}
