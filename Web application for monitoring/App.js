import React from "react";
import ReactDOM from "react-dom";
import Map from "./components/Map";
import styles from "./styles/global.css";
import { io } from "socket.io-client";
import { useState, useEffect } from "react";

const App = () => {
  const [containers, setContainers] = useState([]);
  const [newDataAvailable, setNewDataAvailable] = useState(false);
  useEffect(() => {
    const socket = io();
    socket.on("newDataAvailable", () => {
      setNewDataAvailable(true);
    });
    fetch("/activeDevices")
      .then((res) => res.json())
      .then((data) => setContainers(Object.values(data)));
  }, []);
  useEffect(() => {
    if (newDataAvailable) {
      fetch("/activeDevices")
        .then((res) => res.json())
        .then((data) => setContainers(Object.values(data)));
      setNewDataAvailable(false);
    }
  }, [newDataAvailable]);
  return (
    <>
      <h1 className="heading">Garbage Monitoring with CNN</h1>
      <Map newDataAvailable={newDataAvailable} containers={containers} />
    </>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));
