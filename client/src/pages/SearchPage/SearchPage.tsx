import { useState } from "react";
import "semantic-ui-css/semantic.min.css";
import { createMedia } from "@artsy/fresnel";

import "./styles.css";
import "leaflet/dist/leaflet.css";

import {
  Button,
  Container,
  Dropdown,
  Form,
  Grid,
  Menu,
  Segment,
  Input,
  Visibility,
} from "semantic-ui-react";
import { searchStopsByName } from "../../services/StopsService";
import { searchRoutesDepature } from "../../services/RoutesService";
import { useNavigate } from 'react-router-dom'

const { Media } = createMedia({
  breakpoints: {
    mobile: 0,
    tablet: 768,
    computer: 1024,
  },
});

export default function SearchPage() {
  const navigate = useNavigate()

  const [fixed, setFixed] = useState(false);

  const [from, setFrom] = useState("");

  const [to, setTo] = useState("");

  const [fromId, setFromId] = useState("");

  const [toId, setToId] = useState("");

  const [at, setAt] = useState("");

  const [mode, setMode] = useState("dep");

  const [fromOptions, setFromOptions] = useState([]);

  const [toOptions, setToOptions] = useState([]);

  const [isLoading, setIsLoading] = useState(false);

  const hideFixedMenu = () => setFixed(false);
  const showFixedMenu = () => setFixed(true);

  const onFromSearchChange = (e, data) => {
    setFrom(data.searchQuery);
    search(data.searchQuery, setFromOptions);
  };

  const search = async (searchText, setOptions) => {
    try {
      if (searchText.length >= 3) {
        setIsLoading(true);
        const res = await searchStopsByName(searchText);
        setOptions(
          res.data.map((d) => ({
            ...d,
            value: d.stop_id,
            key: d.stop_id,
            text: d.stop_name,
          }))
        );
        setIsLoading(false);
      }
    } catch (e) {
      console.log(e);
    }
  };

  const handleFromChange = (e, { value }) => {

    const from_obj = fromOptions.find((o) => o.stop_id === value);
    setFrom(from_obj?.stop_name + " - " + from_obj?.stop_id);
    setFromId(from_obj?.stop_id);
  };

  const onToSearchChange = (e, data) => {
    setTo(data.searchQuery);
    search(data.searchQuery, setToOptions);
  };

  const handleToChange = (e, { value }) => {
    const to_obj = toOptions.find((o) => o.stop_id === value);
    setTo(to_obj?.stop_name + " - " + to_obj?.stop_id);
    setToId(to_obj?.stop_id);
  };

  const searchRoute = async () => {
    if (mode === "dep") {
      navigate(`/result?from=${fromId}&to=${toId}&dep=${at}`)
    } else {
      navigate(`/result?from=${fromId}&to=${toId}&arr=${at}`)
    }
  };

  return (
    <Media greaterThan="mobile">
      <Visibility
        once={false}
        onBottomPassed={showFixedMenu}
        onBottomPassedReverse={hideFixedMenu}
      >
        <Segment
          inverted
          textAlign="center"
          style={{ height: "100vh", padding: "1em 0em" }}
          vertical
        >
          <Menu
            fixed={fixed ? "top" : null}
            inverted={!fixed}
            pointing={!fixed}
            secondary={!fixed}
            size="large"
          >
            <Container>
              <Menu.Item as="a" active>
                Home
              </Menu.Item>
              <Menu.Item as="a">About</Menu.Item>
            </Container>
          </Menu>
          <Container className="container">
            <Grid className="main">
              <Grid.Row columns={2}>
                <Grid.Column mobile={16} computer={16}>
                  <Form>
                    <Grid>
                      <Grid.Row>
                        <Button
                          onClick={() => setMode("dep")}
                          content="Departure At"
                          primary={mode === "dep"}
                          secondary={mode === "arr"}
                        />
                        <Button
                          onClick={() => setMode("arr")}
                          content="Arrival At"
                          primary={mode === "arr"}
                          secondary={mode === "dep"}
                        />
                      </Grid.Row>
                      <Grid.Row>
                        <Dropdown
                          placeholder="From..."
                          fluid
                          search
                          selection
                          options={fromOptions}
                          className="searchPosition"
                          value={from}
                          searchQuery={from}
                          onSearchChange={onFromSearchChange}
                          onChange={handleFromChange}
                          loading={isLoading}
                        />
                      </Grid.Row>
                      <Grid.Row>
                        <Dropdown
                          placeholder="To..."
                          fluid
                          search
                          selection
                          options={toOptions}
                          className="searchPosition"
                          value={to}
                          searchQuery={to}
                          onSearchChange={onToSearchChange}
                          onChange={handleToChange}
                          loading={isLoading}
                        />
                      </Grid.Row>
                      <Grid.Row>
                        <Input
                            placeholder={mode === 'dep' ? 'Depature at ...' : 'Arrival at ...'}
                            value={at}
                            onChange={(e) => setAt(e.target.value)}
                        />
                      </Grid.Row>
                      <Grid.Row>
                        <Button content="Find" primary onClick={searchRoute} />
                      </Grid.Row>
                    </Grid>
                  </Form>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Container>
        </Segment>
      </Visibility>
    </Media>
  );
}
