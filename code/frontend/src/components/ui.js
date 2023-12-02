import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Flex,
  Heading,
  Input,
  Link,
  Text,
} from "@chakra-ui/react";
import Card from "../components/card.js";

function convertCardValue(value) {
  const valueMap = { J: 11, Q: 12, K: 13, T: 10 };
  return valueMap[value] || parseInt(value, 10) || null;
}

const GameUi = (props) => {
  const user = props.location.state;
  const [turn, setTurn] = useState(user.lobbyTurn);
  const [ante, setAnte] = useState(25);
  const [pHand, setPHand] = useState([
    ["2", "S"],
    ["2", "D"],
    ["2", "H"],
  ]);
  const [dHand, setDHand] = useState([
    ["8", "S"],
    ["8", "D"],
    ["8", "H"],
  ]);
  const [cardsDealt, setCardsDealt] = useState(false);

  const deal = () => {
    axios
      .post(
        `http://localhost:8000/deal-cards?lobby_id=${parseInt(
          user.lobbyId
        )}&ante_amount=${ante}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      )
      .then((res) => {
        console.log("Response:", res.data);
        setTurn(res.data.turn);
        setCardsDealt(true);
        setPHand(res.data.playerHand);
        setDHand(res.data.lobbyHand);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <Flex p={4} width="100vw" minHeight="80vh">
      <Flex width="20%" flexDirection="column">
        <Flex
          m={4}
          flexDirection="column"
          background="white"
          borderRadius="5px"
          boxShadow="md"
        >
          <Flex justifyContent="space-between" p={2}>
            <Text fontSize="2xl" textTransform="capitalize" fontWeight="bold">
              {user.firstname + " " + user.lastname}
            </Text>
          </Flex>
          <Flex justifyContent="space-between" px={2}>
            <Text fontSize="xs">Lobby ID</Text>
            <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
              {user.lobbyId}
            </Text>
          </Flex>
          <Flex justifyContent="space-between" px={2}>
            <Text fontSize="xs">Turn #</Text>
            <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
              {turn}
            </Text>
          </Flex>
        </Flex>
        <Flex
          m={4}
          flexDirection="column"
          background="white"
          borderRadius="5px"
          boxShadow="md"
        >
          <Flex justifyContent="space-between" p={2}>
            <Text fontWeight="bold">BALANCE</Text>
            <Link>Reset</Link>
          </Flex>
          <Heading p={2} fontWeight="bold" color="orange.300">
            ${user.balance}
          </Heading>
        </Flex>
        <Flex
          m={4}
          flexDirection="column"
          background="white"
          borderRadius="5px"
          boxShadow="md"
        >
          <Flex justifyContent="space-between" p={2}>
            <Text fontWeight="bold">PLAYER STATS</Text>
          </Flex>
          <Flex flexDirection="column">
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Games Played</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Turns Played</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Wins</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Losses</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Win Ratio</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Plays</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Folds</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
            <Flex justifyContent="space-between" px={2}>
              <Text fontSize="xs">Play / Fold Ratio</Text>
              <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                0
              </Text>
            </Flex>
          </Flex>
        </Flex>
      </Flex>
      <Flex width="80%" backgroundColor="#B3DDC9" justifyContent="center">
        <Flex width="80%" flexDirection="column">
          <Flex flex={1} justifyContent="flex-start" alignItems="center">
            <Card number="2" suit="S" />
            <Card number="2" suit="H" />
            <Card number="2" suit="C" />
          </Flex>
          <Flex flex={1} flexDirection="column" alignItems="center">
            <Flex
              position="relative"
              width="90%"
              justifyContent="center"
              alignItems="center"
            >
              <Box
                position="absolute"
                height="4px"
                left="10px"
                right="10px"
                backgroundColor="white"
                zIndex="2"
              />
              <Text
                p="2"
                fontWeight="bold"
                fontSize="lg"
                backgroundColor="#B3DDC9"
                zIndex="4"
              >
                Dealer Hand
              </Text>
            </Flex>
            <Heading
              width="60%"
              fontSize="5xl"
              textAlign="center"
              fontWeight="bold"
              color="white"
              my="5"
            >
              Dealer plays with Queen High or Better
            </Heading>
            <Flex
              position="relative"
              width="90%"
              justifyContent="center"
              alignItems="center"
            >
              <Box
                position="absolute"
                height="4px"
                left="10px"
                right="10px"
                backgroundColor="white"
                zIndex="2"
              />
              <Text
                p="2"
                fontWeight="bold"
                fontSize="lg"
                backgroundColor="#B3DDC9"
                zIndex="4"
              >
                Player Hand
              </Text>
            </Flex>
          </Flex>
          <Flex flex={1} justifyContent="center" alignItems="center">
            <Flex flexDirection="column" alignItems="center">
              <Flex m="2" alignItems="center" justifyContent="center">
                <Heading size="md" m={2}>
                  Ante $
                </Heading>
                <Input
                  m={2}
                  flex={0.2}
                  type="number"
                  background="white"
                  boxShadow="outline"
                  value={ante}
                  onChange={(e) => setAnte(e.target.value)}
                />
              </Flex>
              {/* <Flex
              position="relative"
              width="90%"
              justifyContent="center"
              alignItems="center"
            >
              <Box
                position="absolute"
                height="2px"
                left="10px"
                right="10px"
                backgroundColor="white"
                zIndex="2"
              />
            </Flex> */}
              <Flex m="2" alignItems="center">
                <Button
                  w="100px"
                  variant="solid"
                  size="md"
                  m={1}
                  isDisabled={cardsDealt}
                  onClick={() => deal()}
                >
                  Deal
                </Button>
                <Button
                  width="60px"
                  variant="solid"
                  size="sm"
                  m={1}
                  isDisabled={!cardsDealt}
                >
                  Play
                </Button>
                <Button
                  width="60px"
                  variant="solid"
                  size="sm"
                  m={1}
                  isDisabled={!cardsDealt}
                >
                  Fold
                </Button>
              </Flex>
            </Flex>
            <Flex>
              <Card
                number={convertCardValue(pHand[0][0])}
                suit={pHand[0][1].charAt(0)}
                side={cardsDealt ? "" : "back"}
              />
              <Card
                number={convertCardValue(pHand[1][0])}
                suit={pHand[1][1].charAt(0)}
                side={cardsDealt ? "" : "back"}
              />
              <Card
                number={convertCardValue(pHand[2][0])}
                suit={pHand[2][1].charAt(0)}
                side={cardsDealt ? "" : "back"}
              />
            </Flex>
          </Flex>
        </Flex>
      </Flex>
    </Flex>
  );
};

export default GameUi;
