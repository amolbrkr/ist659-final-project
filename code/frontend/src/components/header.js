import React from "react";
import { Flex, Text } from "@chakra-ui/react";

const Header = () => (
  <Flex
    justifyContent="space-between"
    alignItems="center"
    backgroundColor="whatsapp.500"
    color="whiteAlpha.500"
    p="2"
  >
    <Text color="white" fontSize="2xl">
      Three Card Poker
    </Text>
    <Flex>
      <Text color="white">Username</Text>
      <Text ml={2} fontWeight="bold" color="orange.500">
        $100
      </Text>
    </Flex>
  </Flex>
);

export default Header;
