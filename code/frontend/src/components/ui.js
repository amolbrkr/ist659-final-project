import React, { useState, useEffect } from "react";
import axios from "axios";
import { navigate } from "@reach/router";
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
  const valueMap = { J: 11, Q: 12, K: 13, T: 10, A: "A" };
  let x = valueMap[value] || value;
  console.log(x);
  return x;
}

const GameUi = (props) => {
  const user = props.location.state;
  const [turn, setTurn] = useState(user.lobbyTurn);
  const [balance, setBalance] = useState(user.balance);
  const [ante, setAnte] = useState(25);
  const [outcome, setOutcome] = useState("");
  const [showOutcome, setShowOutcome] = useState(false);
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
  const [showDCards, setShowDCards] = useState(false);
  const [stats, setStats] = useState(null);

  const updateStats = () => {
    axios
      .post(
        `http://localhost:8000/get-stats?player_id=${parseInt(user.player)}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      )
      .then((res) => {
        console.log("Response:", res.data);
        setStats(res.data);
        setBalance(res.data.balance);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  const resetBalance = () => {
    axios
      .post(
        `http://localhost:8000/set-balance?player_id=${parseInt(user.player)}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      )
      .then((res) => {
        console.log("Response:", res.data);
        setBalance(res.data.balance);
      })
      .catch((err) => {
        console.error(err);
      });
  };

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

  const play = () => {
    axios
      .post(
        `http://localhost:8000/play?lobby_id=${user.lobbyId}&turn=${turn}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      )
      .then((res) => {
        console.log("Response:", res.data);
        setBalance(res.data.balance);
        setOutcome(res.data.outcome.replace("_", " ") + "s");
        setShowOutcome(true);
        setShowDCards(true);
        updateStats();
        setTimeout(() => {
          setCardsDealt(false);
          setShowDCards(false);
          setShowOutcome(false);
        }, 8000);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  const fold = () => {
    axios
      .post(
        `http://localhost:8000/fold?lobby_id=${user.lobbyId}&turn=${turn}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      )
      .then((res) => {
        console.log("Response:", res.data);
        // setBalance(res.data.balance);
        setOutcome(res.data.outcome.replace("_", " ") + "s");
        setShowOutcome(true);
        setShowDCards(true);
        updateStats();
        setTimeout(() => {
          setCardsDealt(false);
          setShowDCards(false);
          setShowOutcome(false);
        }, 8000);
      })
      .catch((err) => {
        console.error(err);
      });
  };
  const exit = () => {
    axios
      .post(`http://localhost:8000/exit?lobby_id=${user.lobbyId}`, {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      })
      .then((res) => {
        console.log("Response:", res.data);
        navigate("/", { replace: true });
      })
      .catch((err) => {
        console.error(err);
      });
  };

  useEffect(() => {
    updateStats();
  }, []);

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
            <Link onClick={() => exit()}>Log out</Link>
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
            <Link onClick={() => resetBalance()}>Reset</Link>
          </Flex>
          <Heading p={2} fontWeight="bold" color="orange.300">
            ${balance}
          </Heading>
        </Flex>
        {stats && (
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
                  {stats.gamesPlayed}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Turns Played</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.turnsPlayed}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Wins</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.wins}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Losses</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.defeats}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Win Ratio</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.winRatio}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Plays</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.plays}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Folds</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.folds}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Play Ratio</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.playRatio}
                </Text>
              </Flex>
              <Flex justifyContent="space-between" px={2}>
                <Text fontSize="xs">Fold Ratio</Text>
                <Text fontSize="md" fontWeight="bold" color="blackAlpha.500">
                  {stats.foldRatio}
                </Text>
              </Flex>
            </Flex>
          </Flex>
        )}
      </Flex>
      <Flex width="80%" backgroundColor="#B3DDC9" justifyContent="center">
        <Flex width="80%" flexDirection="column">
          <Flex flex={1} justifyContent="flex-start" alignItems="center">
            <Card
              number={convertCardValue(dHand[0][0])}
              suit={dHand[0][1].charAt(0)}
              side={showDCards ? "" : "back"}
            />
            <Card
              number={convertCardValue(dHand[1][0])}
              suit={dHand[1][1].charAt(0)}
              side={showDCards ? "" : "back"}
            />
            <Card
              number={convertCardValue(dHand[2][0])}
              suit={dHand[2][1].charAt(0)}
              side={showDCards ? "" : "back"}
            />
            {showOutcome && (
              <Flex
                mx="50px"
                flexDirection="column"
                justifyContent="center"
                alignItems="center"
                width="300px"
                minHeight="200px"
                backgroundColor="blackAlpha.800"
                color="white"
                borderRadius={28}
                opacity={1}
                boxShadow="md"
              >
                <Heading mt={4} mb={4} textTransform="capitalize">
                  {outcome}
                </Heading>
                <Text>0</Text>
              </Flex>
            )}
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
                  onClick={() => play()}
                >
                  Play
                </Button>
                <Button
                  width="60px"
                  variant="solid"
                  size="sm"
                  m={1}
                  isDisabled={!cardsDealt}
                  onClick={() => fold()}
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
