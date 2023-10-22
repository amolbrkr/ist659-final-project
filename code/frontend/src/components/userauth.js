import {
  Button,
  Flex,
  Input,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";

const UserAuth = () => (
  <Flex
    minHeight="40vh"
    p="4"
    bg="white"
    borderRadius="10px"
    align="flex-start"
    justify="center"
  >
    <Tabs size="md" isFitted width="40vh" colorScheme="green">
      <TabList>
        <Tab panelId="login">Login</Tab>
        <Tab panelId="signup">Sign up</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>
          <Flex flexDirection="column" alignItems="center">
            <Input placeholder="Username" mb={2} />
            <Input type="password" placeholder="Password" mb={2} />
            <Button variant="solid" size="md">
              Login
            </Button>
          </Flex>
        </TabPanel>
        <TabPanel>
          <Flex flexDirection="column" alignItems="center">
            <Input placeholder="First name" mb={2} />
            <Input placeholder="Last name" mb={2} />
            <Input placeholder="Username" mb={2} />
            <Input type="password" placeholder="Password" mb={2} />
            <Button variant="solid" size="md">
              Register
            </Button>
          </Flex>
        </TabPanel>
      </TabPanels>
    </Tabs>
  </Flex>
);

export default UserAuth;
