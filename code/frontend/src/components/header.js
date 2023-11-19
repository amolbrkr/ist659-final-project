import React from "react";
import { Flex, Text } from "@chakra-ui/react";

const Header = () => (
  <Flex
    justifyContent="space-between"
    alignItems="center"
    backgroundColor="green.500"
    position="fixed"
    width="100%"
    boxShadow="md"
    color="whiteAlpha.500"
    p="2"
  >
    <Text fontWeight="bold" color="white" fontSize="2xl">
      Three Card Poker
    </Text>
    <Flex align="center">
      <Text color="white">Username</Text>
      <Text ml="2" fontSize="xl" fontWeight="bold" color="orange">
        $100
      </Text>
    </Flex>
  </Flex>
);

export default Header;
