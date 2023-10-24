import React from 'react'
import {
  ChakraProvider,
  Input,
  Heading,
  Flex,
  Image,
  Button
} from '@chakra-ui/react'

const App = () => (
  <ChakraProvider resetCSS>
    <Flex flexDirection="column">
      <Flex>
        <Flex>
          <Image height="100px" width="100px" />
          <Image height="100px" width="100px" ml={10} mr={10} />
          <Image height="100px" width="100px" />
        </Flex>
      </Flex>
      <Flex>
        <Heading display="flex" size="xl" textAlign="center" color="gray.500">
          Dealer plays with Queen hand or better
        </Heading>
      </Flex>
      <Flex justifyContent="flex-start" flexDirection="row">
        <Flex flexDirection="column" width="20%">
          <Heading
            as="h1"
            isTruncated
            size="lg"
            display="flex"
            justifyContent="center"
            width={11}
          >
            Ante
          </Heading>
          <Input />
        </Flex>
        <Flex flexDirection="column" width="80%">
          <Heading
            as="h1"
            isTruncated
            size="lg"
            display="flex"
            justifyContent="center"
            width={11}
          >
            Hand
          </Heading>
          <Flex alignItems="space-between">
            <Image height="100px" width="100px" />
            <Image height="100px" width="100px" ml={4} mr={4} />
            <Image
              height="100px"
              width="100px"
              display="flex"
              alignItems="center"
            />
          </Flex>
          <Flex alignItems="space-between">
            <Button variant="solid" size="md">
              Deal
            </Button>
            <Button variant="solid" size="md" ml={55} mr={55}>
              Play
            </Button>
            <Button variant="solid" size="md">
              Fold
            </Button>
          </Flex>
        </Flex>
      </Flex>
    </Flex>
  </ChakraProvider>
)

export default App