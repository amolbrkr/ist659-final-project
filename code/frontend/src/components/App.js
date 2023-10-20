import { Global } from "@emotion/react";
import { ChakraProvider, extendTheme, Flex } from "@chakra-ui/react";
import { Router } from "@reach/router";

import Header from "./header.js";
import UserAuth from "./userauth.js";

const Fonts = () => (
  <Global
    styles={`
      /* latin */
      @font-face {
        font-family: 'Caprasimo';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.googleapis.com/css2?family=Caprasimo&display=swap) format('woff');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
      }
      `}
  />
);

const theme = extendTheme({
  fonts: {
    heading: "Caprasimo",
    body: "Caprasimo",
  },
});

const App = () => {
  return (
    <ChakraProvider theme={theme}>
      <Fonts />
      <Header />
      <Flex justify="center" align="center" height="100vh" bg="#b3ddc9">
        <Router>
          <UserAuth path="/" />
        </Router>
      </Flex>
    </ChakraProvider>
  );
};

export default App;
