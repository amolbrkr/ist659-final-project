import React from "react";

const Card = ({ card }) => {
  return (
    <div>
      <svg
        width="300"
        height="200"
      >
        <use href="svg-cards.svg#back" x="150" y="10" fill="red" />
      </svg>
    </div>
  );
};

export default Card;
