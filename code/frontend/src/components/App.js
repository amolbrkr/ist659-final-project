import { ChakraProvider } from "@chakra-ui/react";

import Header from "./header.js";

function App() {
  return (
    <ChakraProvider>
      <div className="App">
        <Header />
      </div>
    </ChakraProvider>
  );
}

export default App;
