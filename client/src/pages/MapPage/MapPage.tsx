import React, { useEffect, useState } from "react";
import "semantic-ui-css/semantic.min.css";
import { createMedia } from "@artsy/fresnel";

import "./styles.css";

import {
  Container,
  Menu,
  Segment,
  Visibility,
  Grid,
  Form,
} from "semantic-ui-react";
import {
  searchRoutesArrival,
  searchRoutesDepature,
} from "../../services/RoutesService";
import { Link, useLocation } from "react-router-dom";
import ResultMap from '../../components/Map';

const { Media } = createMedia({
  breakpoints: {
    mobile: 0,
    tablet: 768,
    computer: 1024,
  },
});

const defaultPosition = {
  lat: 45.764,
  lng: 4.8357,
  zoom: 13,
};

const metroColors = {
  A: "#f161ad",
  B: "#48a2d5",
  C: "#f99d1d",
  D: "#00ac4d",
};

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}


export default function MapPage() {
  const parisPosition: [number, number] = [
    defaultPosition.lat,
    defaultPosition.lng,
  ];

  const query = useQuery();

  const [fixed, setFixed] = useState(false);

  const [routes, setRoutes] = useState<any>(null);

  const [markers, setMarkers] = useState<any>([]);

  const [polyline, setPolyline] = useState([]);

  const hideFixedMenu = () => setFixed(false);
  const showFixedMenu = () => setFixed(true);

  useEffect(() => {

    const search = async () => {
      const from = query.get("from")
      const to = query.get("to")
      const dep = query.get("dep")
      const arr = query.get("arr")

      let res = null;

      if (dep) {
        res = await searchRoutesDepature(from, to, dep);
      } else {
        res = await searchRoutesArrival(from, to, arr);
      }

      setRoutes(res.data[0] || null);

      for (let i = 0; i < res?.data[0]?.journeys.length; i++) {
        setMarkers((prev) => [
          ...prev,
          res?.data[0]?.journeys?.[i]?.start_station,
        ]);

        if (res?.data[0]?.journeys?.[i]?.next_station) {
          for (
            let j = 0;
            j < res?.data[0]?.journeys?.[i]?.next_station.length;
            j++
          ) {
            setMarkers((prev) => [
              ...prev,
              res?.data[0]?.journeys?.[i]?.next_station[j],
            ]);
          }
        }

        if (res?.data[0]?.journeys?.[i]?.end_station) {
          setMarkers((prev) => [
            ...prev,
            res?.data[0]?.journeys?.[i]?.end_station,
          ]);
        }

        setPolyline((prev) => {
          const copy = [...prev];

          const temp = [];

          temp.push([
            res?.data[0]?.journeys?.[i]?.start_station.lat,
            res?.data[0]?.journeys?.[i]?.start_station.lon,
          ]);

          if (res?.data[0]?.journeys?.[i]?.next_station) {
            for (
              let j = 0;
              j < res?.data[0]?.journeys?.[i]?.next_station.length;
              j++
            ) {
              temp.push([
                res?.data[0]?.journeys?.[i]?.next_station[j].lat,
                res?.data[0]?.journeys?.[i]?.next_station[j].lon,
              ]);
            }
          }

          if (res?.data[0]?.journeys?.[i]?.end_station) {
            temp.push([
              res?.data[0]?.journeys?.[i]?.end_station.lat,
              res?.data[0]?.journeys?.[i]?.end_station.lon,
            ]);
          }

          copy.push({
            transport: res?.data[0]?.journeys?.[i]?.transport,
            trips: temp,
          });

          return copy;
        });
      }
    }

    search()
  }, [])

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
              <Menu.Item as="a">
                <Link to={'/'}>
                  Home
                </Link>
              </Menu.Item>
            </Container>
          </Menu>
          <Container className="container result">

            <Form className={"routes-wrapper"}>
              <Grid>
                <Grid.Row>
                  <div className="routes">
                    <div className="route-names">
                      {routes?.journeys?.map((route) =>
                        route?.transport ? (
                          <div
                            className={"route-name"}
                            key={route.transport}
                            style={{
                              backgroundColor: `${metroColors[route?.transport]
                                }`,
                            }}
                          >
                            {route?.transport}
                          </div>
                        ) : (
                          <div className={"route-name"} key={route.transport}>W</div>
                        )
                      )}
                    </div>
                    <div>
                      {routes?.journeys?.map((route) =>
                        route?.transport ? (
                          <div className="trip" key={route.transport}>
                            <h2>{route.transport}</h2>
                            <p>{route?.start_station?.name}</p>
                            <p>•</p>
                            {route?.next_station?.map((station) => (
                              <>
                                <p>{station?.name}</p>
                                <p>•</p>
                              </>
                            ))}
                            <p>{route?.end_station?.name}</p>
                          </div>
                        ) : (
                          <div className="trip" key={route.transport}>
                            <h2>Walking</h2>
                            <p>{route?.start_station?.name}</p>
                            <p>•</p>
                            {route?.next_station?.map((station) => (
                              <>
                                <p>{station?.name}</p>
                                <p>•</p>
                              </>
                            ))}
                            <p>{route?.end_station?.name}</p>
                          </div>
                        )
                      )}
                    </div>
                    <div className="totalTimeWrapper">
                      <p>
                        Total travel time:{" "}
                        <span className="totalTime">
                          {routes?.total_travel_times}
                        </span>
                      </p>
                    </div>
                  </div>
                </Grid.Row>
              </Grid>
            </Form>

            <Grid className="main">
              <Grid.Row columns={2}>
                <Grid.Column mobile={16} computer={16}>
                  <ResultMap polyline={polyline} markers={markers} />
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </Container>
        </Segment>
      </Visibility>
    </Media>
  );
}