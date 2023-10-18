import logo from './logo.svg';
import './App.css';

import logo from './logo.svg';
import './App.css';



import React, { Component } from 'react';





class ThreeCardPoker extends Component {
  constructor(props) {
    super(props);
    this.state = {
      playerHand: [],
      dealerHand: [],
      result: '',
    };
  };

  componentDidMount() {
    this.dealCards();
  }

  dealCards = () => {
    // Simulate dealing cards (you can replace this with your logic)
    const playerHand = this.getRandomCards(3);
    const dealerHand = this.getRandomCards(3);

    this.setState({
      playerHand,
      dealerHand,
      result: '',
    });
  };

  getRandomCards = (numCards) => {
    const cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    const suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'];
    const hand = [];

    while (hand.length < numCards) {
      const randomCard = cards[Math.floor(Math.random() * cards.length)];
      const randomSuit = suits[Math.floor(Math.random() * suits.length)];
      const card = `${randomCard} of ${randomSuit}`;
      
      if (!hand.includes(card)) {
        hand.push(card);
      }
    }

    return hand;
  };

  evaluateHands = () => {
    // Add your hand evaluation logic here to determine the winner
    // Update the result state accordingly
  };

  render() {
    const { playerHand, dealerHand, result } = this.state;

    return (
      <div>
        <h1>3 Card Poker</h1>
        <button onClick={this.dealCards}>Deal</button>
        <div>
          <h2>Player Hand:</h2>
          <ul>
            {playerHand.map((card, index) => (
              <li key={index}>{card}</li>
            ))}
          </ul>
        </div>
        <div>
          <h2>Dealer Hand:</h2>
          <ul>
            {dealerHand.map((card, index) => (
              <li key={index}>{card}</li>
            ))}
          </ul>
        </div>
        {result && <div>Result: {result}</div>}
      </div>
    );
  }
}

export default ThreeCardPoker;




// Log to console
console.log('Hello console')
