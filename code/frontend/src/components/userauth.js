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
import axios from "axios";
import { navigate } from "@reach/router";

const UserAuth = () => {
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [uname, setUname] = useState("");
  const [pwd, setPwd] = useState("");
  const [status, setStatus] = useState("");

  const handleLogin = () => {
    console.log(uname, pwd);
    axios.post("http://localhost:8000/login", {
      "username": uname,
      "password": pwd,
    }, {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((res) => {
        console.log("Response:", res.data);
        if (res.data.loginSuccess === true) navigate("/game", {replace: true})
      })
      .catch((err) => {
        console.error(err);
        setStatus(`Error: ${err.response.data.detail}`);
      });
  };

  const handleSignup = () => {
    console.log(fname, lname, uname, pwd);
    axios.post("http://localhost:8000/create-player", {
      "firstname": fname,
      "lastname": lname,
      "username": uname,
      "password": pwd,
    }, {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((res) => {
        console.log("Response:", res.data);
        if (res.status === 200) {
          setStatus(
            "Success: Player created, please login using your username.",
          );
        }
      })
      .catch((err) => {
        console.error(err);
        setStatus(`Error: ${err.response.data.detail}`);
      });
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
      <Tabs size="md" isFitted width="45wh" colorScheme="green">
        <TabList>
          <Tab>Login</Tab>
          <Tab>Sign up</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Flex m="2" justify="center">
              <Text size="md">{status}</Text>
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
              <Text size="md">{status}</Text>
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
