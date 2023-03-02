import L from "leaflet";

let containerIcon = L.icon({
  iconUrl: "/static/icons/trashcan.png",
  iconSize: [23, 40],
  popupAnchor: [0, -20],
  shadowSize: [68, 95],
  shadowAnchor: [22, 94],
});

let alertContainerIcon = L.icon({
  iconUrl: "/static/icons/trashcan_alert.png",
  iconSize: [35, 35],
  popupAnchor: [0, -20],
  shadowSize: [68, 95],
  shadowAnchor: [22, 94],
});

export { containerIcon, alertContainerIcon };
