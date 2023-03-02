import React, { useState } from "react";
import { useEffect } from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

export default function ContainerDashboard(props) {
  const { id, latlng, fullness } = props;
  const [imagePaths, setImagePaths] = useState([]);
  useEffect(() => {
    fetch(`/getImagePaths?id=${id}`)
      .then((res) => res.json())
      .then((paths) => setImagePaths(paths));
  }, []);
  useEffect(() => {
    fetch(`/getImagePaths?id=${id}`)
      .then((res) => res.json())
      .then((paths) => setImagePaths(paths));
  }, [props.newDataAvailable]);
  return (
    <>
      <Card
        elevation={20}
        sx={{
          maxWidth: 450,
          minHeight: 400,
          maxHeight: 700,
          minWidth: 350,
          position: "fixed",
          zIndex: 1000,
          bottom: 0,
          right: 10,
          boxShadow: "0px 3px 10px 1px #5c5c5cbd",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
            justifyItems: "center",
            gap: 10,
            margin: 10,
            paddingBottom: 120,
          }}
        >
          {imagePaths.map((filename) => {
            let timestamp = filename.match(/\d{8}_\d{6}/)[0];
            const date = new Date(
              `${timestamp.substr(0, 4)}-${timestamp.substr(
                4,
                2
              )}-${timestamp.substr(6, 2)}T` +
                `${timestamp.substr(9, 2)}:${timestamp.substr(
                  11,
                  2
                )}:${timestamp.substr(13, 2)}`
            );
            let time = `${date.getHours()} : ${date.getMinutes()} : ${date.getSeconds()}`;
            return (
              <div key={`image_${filename}`}>
                <img
                  style={{
                    boxShadow: "0 0 10px 1px #979292",
                    height: 150,
                    width: 150,
                  }}
                  src={`/getImage?id=${id}&filename=${filename}`}
                />
                <div
                  style={{
                    textAlign: "center",
                    padding: 5,
                    fontWeight: "bold",
                    color: "grey",
                  }}
                >
                  {time}
                </div>
              </div>
            );
          })}
        </div>
        <CardContent sx={{ position: "absolute", bottom: 0 }}>
          <Typography gutterBottom variant="h5" component="div">
            Container <b>{id}</b>
          </Typography>
          <Typography variant="body2" color="text.secondary">
            <span style={{ display: "block" }}>Fullness: {fullness}</span>
          </Typography>
        </CardContent>
      </Card>
    </>
  );
}
