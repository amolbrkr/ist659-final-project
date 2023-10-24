import React from "react";
const f = (x) => {
  if (x == 1) return "A";
  if (x <= 10) return x;
  return "J,Q,K".split(",")[x - 11];
};
const Card = ({ number, suit }) => {
  const style = {
    width: "calc(100vw/14)",
    margin: "2px"
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
    <img onClick={() => setImgUrl("")} style={style} src={imgUrl} />
  );
};
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

export default Card;

  