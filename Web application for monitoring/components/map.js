import L from "leaflet";
import React from "react";
import { useState, useEffect } from "react";
import Container from "./container";
import Paper from "@mui/material/Paper";

const Map = (props) => {
  const [map, setMap] = useState();
  const { containers } = props;
  useEffect(() => {
    let mapObject = L.map("map", {
      center: [27.7172, 85.324],
      attributionControl: false,
      zoom: 12,
      inertia: true,
    });
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(mapObject);
    setMap(mapObject);
  }, []);

  return (
    <>
      <Paper id="map" elevation={20}>
        {containers.map((container) => (
          <Container
            map={map}
            id={container.id}
            newDataAvailable={props.newDataAvailable}
            latlng={container.latlng}
            fullness={container.fullness}
            key={`container${container.id}`}
          />
        ))}
      </Paper>
    </>
  );
};

export default Map;
