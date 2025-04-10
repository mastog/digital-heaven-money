
import { useEffect, useRef } from 'react';
import Typed from 'typed.js';

export default function HeroIsland({ strings }) {
  const el = useRef(null);

  useEffect(() => {
    const typed = new Typed(el.current, {
      strings,
      typeSpeed: 30,
      startDelay: 300,
      loop: false,
      showCursor: false,
      backSpeed: 0
    });

    return () => typed.destroy();
  }, [strings]);

  return <div ref={el} className="text-4xl font-bold" />;
}
