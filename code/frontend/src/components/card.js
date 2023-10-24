import React from 'react';

function SvgCards() {
  return (
    <div>
      <h1>Example SVG with cards</h1>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="48"
        height="48"
        fill={fillColor}
        class="bi bi-google"
        viewBox="0 0 16 16"
      >
        {/* Your SVG content here */}
        <use href="node_modules/svg-cards/svg-cards.svg#back" x="150" y="10" fill="red" />
        <use href="node_modules/svg-cards/svg-cards.svg#heart_1" x="0" y="0" />
        <use href="node_modules/svg-cards/svg-cards.svg#joker_black" x="100" y="100" />
        <use
          href="node_modules/svg-cards/svg-cards.svg#spade_10"
          x="200"
          y="200"
          transform="rotate(45,198.0375,122.320)scale(0.5)"
        />
        <use
          href="svg-cards.svg#club_jack"
          x="300"
          y="100"
          transform="rotate(75,198.0375,122.320)scale(0.75)"
        />
      </svg>
    </div>
  );
}

export default SvgCards;
  