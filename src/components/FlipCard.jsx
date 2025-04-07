import React, { useState, useEffect } from 'react';

const FlipCard = ({ items }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Update the current index and trigger the animation
    const updateFlipCard = () => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % items.length);
    };

    // Set an interval to switch every 2 seconds
    const interval = setInterval(updateFlipCard, 2000);

    // Clean up the interval
    return () => clearInterval(interval);
  }, [items.length]);

  return (
    <div className="flip-card-container relative w-full h-10 flex items-center justify-center overflow-hidden">
      {items.map((item, index) => (
        <span
          key={index}
          className={`flip-card-item absolute w-full h-full flex items-center justify-center text-gray-700 text-center mt-2 transition-all duration-500 transform ${
            index === currentIndex ? 'active' : 'translate-y-full opacity-0'
          }`}
          data-index={index}
        >
          {item}
        </span>
      ))}
    </div>
  );
};

export default FlipCard;