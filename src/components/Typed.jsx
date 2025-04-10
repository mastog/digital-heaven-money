import { useEffect, useState, useRef } from 'react';
import TypedJS from 'typed.js';

export default function Typed({ strings }) {
  const [currentStrings, setCurrentStrings] = useState(strings);
  const elRef = useRef(null);
  const typedRef = useRef(null);

  useEffect(() => {
    if (typedRef.current) {
      typedRef.current.destroy();
    }

    typedRef.current = new TypedJS(elRef.current, {
      strings: currentStrings,
      typeSpeed: 30,
      backSpeed: 0,
      loop: false,
      showCursor: false,
    });

    return () => typedRef.current.destroy();
  }, [currentStrings]);

  useEffect(() => {

    const handler = (e) => {
      if (Array.isArray(e.detail)) {
        setCurrentStrings(e.detail);
      }
    };
    window.addEventListener('update-typed-strings', handler);
    return () => window.removeEventListener('update-typed-strings', handler);
  }, []);

  return <span ref={elRef} className="text-xl font-bold p-10"/>;
}
