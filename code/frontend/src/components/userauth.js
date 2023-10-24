import {
  Button,
  Flex,
  Input,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
} from "@chakra-ui/react";
import { useState } from "react";
import Card from "./card";

const UserAuth = () => {
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [uname, setUname] = useState("");
  const [pwd, setPwd] = useState("");

  const handleLogin = () => {
    console.log(uname, pwd);
  };

  const handleSignup = () => {
    console.log(fname, lname, uname, pwd);
  };

  return (
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
            <Flex m="2" justify="center">
              <Text size="md"></Text>
            </Flex>
            <Flex flexDirection="column" alignItems="center">
              <Input
                placeholder="Username"
                mb={2}
                onChange={(e) => setUname(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Password"
                mb={2}
                onChange={(e) => setPwd(e.target.value)}
              />
              <Button variant="solid" size="md" onClick={handleLogin}>
                Login
              </Button>
            </Flex>
          </TabPanel>
          <TabPanel>
            <Flex m="2" justify="center">
              <Text size="md">Status text goes here</Text>
            </Flex>
            <Flex flexDirection="column" alignItems="center">
              <Input
                placeholder="First name"
                mb={2}
                onChange={(e) => setFname(e.target.value)}
              />
              <Input
                placeholder="Last name"
                mb={2}
                onChange={(e) => setLname(e.target.value)}
              />
              <Input
                placeholder="Username"
                mb={2}
                onChange={(e) => setUname(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Password"
                mb={2}
                onChange={(e) => setPwd(e.target.value)}
              />
              <Button variant="solid" size="md" onClick={handleSignup}>
                Register
              </Button>
            </Flex>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Flex>
  );
};

export default UserAuth;
