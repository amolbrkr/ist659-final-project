import React from 'react';
import Card from './card';

const Hand = ({ cards, title }) => {
  return (
    <div>
      <h2>{title}:</h2>
      <ul>
        {cards.map((card, index) => (
          <li key={index}>
            <Card card={card} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Hand;
