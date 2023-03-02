import React from "react";
import { useState, useEffect } from "react";
import { containerIcon, alertContainerIcon } from "./containerIcon";
import ContainerDashboard from "./containerDashboard";

export default function Container(props) {
  const { id, latlng, fullness, map } = props;
  console.log(id, latlng, fullness);
  const [showDashboard, setShowDashboard] = useState(false);
  useEffect(() => {
    if (!map) return;
    let marker = L.marker(latlng, {
      icon: fullness !== "full" ? containerIcon : alertContainerIcon,
      title: `Container_${id}`,
      alt: "Container",
      riseOnHover: true,
    })
      .addTo(map)
      .bindPopup(
        `
                Fullness: ${fullness} 
              `,
        {
          closeButton: false,
          closeOnClick: false,
          closeOnEscapeKey: false,
          maxWidth: 100,
          autoPan: false,
        }
      )
      .openPopup();

    marker.on("click", (e) => {
      setShowDashboard((prev) => !prev);
      map.setView(e.latlng, 17, {
        animate: true,
        duration: 0.5,
      });
    });
  }, [map, fullness]);
  return (
    <>
      {showDashboard && (
        <ContainerDashboard
          showDashboard={showDashboard}
          id={id}
          newDataAvailable={props.newDataAvailable}
          latlng={latlng}
          fullness={fullness}
        />
      )}
    </>
  );
}
