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

export default function AboutPage() {
  const [fixed, setFixed] = useState(false);

  const hideFixedMenu = () => setFixed(false);
  const showFixedMenu = () => setFixed(true);


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
                  <h1>Hi my name is Quan</h1>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Container>
        </Segment>
      </Visibility>
    </Media>
  );
}
