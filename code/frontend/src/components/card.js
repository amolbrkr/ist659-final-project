import React from "react";
import cardback from "./cardback.png"

const f = (x) => {
  if (x === 1) return "A";
  if (x <= 10) return x;
  return "J,Q,K".split(",")[x - 11];
};

const Card = ({ number, suit, side = "back" }) => {
  const style = {
    width: "calc(100vw/12)",
    margin: "8px",
    borderRadius: "5px",
    boxShadow: "0px 1px 4px 1px rgba(100, 100, 100, 0.25)"
  };
  const [imgUrl, setImgUrl] = React.useState("");
  React.useEffect(() => {
    setImgUrl(
      `https://raw.githubusercontent.com/richardschneider/cardsJS/fe5e857c5094468c58a7cfe0a7075ad351fc7920/cards/${f(
        number
      )}${suit}.svg`
    );
  }, [number, suit]);

  return imgUrl === "" ? null : (
    <img alt="text" style={style} src={side === "back" ? cardback : imgUrl} />
  );
};

export default Card;
