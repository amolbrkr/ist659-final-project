import { ChakraProvider, extendTheme, Flex } from "@chakra-ui/react";
import { Router } from "@reach/router";

import Header from "./header.js";
import UserAuth from "./userauth.js";
import GameUi from "./ui.js";

const theme = extendTheme({
  fonts: {
    heading: "Fondamento",
    body: "Fondamento",
  },
  variants: {
    line: {
      tab: {
        color: "gray.400",
        _selected: {
          color: "gray.100",
        },
      },
    },
  },
});

const App = () => {
  return (
    <ChakraProvider theme={theme}>
      <Header />
      <Flex justify="center" align="center" height="100vh" bg="#b3ddc9">
        <Router>
          <UserAuth path="/" />
          <GameUi path="/game" />
        </Router>
      </Flex>
    </ChakraProvider>
  );
};

export default App;
