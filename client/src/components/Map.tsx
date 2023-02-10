import React from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";

import { Icon } from "leaflet";
import "semantic-ui-css/semantic.min.css";

import "./styles.css";
import "leaflet/dist/leaflet.css";

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

const parisPosition: [number, number] = [
  defaultPosition.lat,
  defaultPosition.lng,
];

interface IResultMap {
  polyline: any
  markers: any
}


export default function ResultMap({
  polyline,
  markers
}: IResultMap) {
  return (
    <MapContainer
      center={parisPosition}
      zoom={12}
      scrollWheelZoom={false}
      className="parisMap"
    >
      <TileLayer
        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {markers.map((marker) => (
        <Marker
          position={[marker?.lat, marker?.lon]}
          key={marker?.name}
          icon={
            " - ".split(" - ")[0] === marker.name
              ? new Icon({
                iconUrl:
                  "https://www.citypng.com/public/uploads/small/11641513638sanpg6vtthzma5pmyxbnbe0sfhpnqdawfg2pjpzl11hkj9qhwbj7g0ektsxgghfjeml4jehzbjkaujbydzfrhf4nb9agagomf0yz.png",
                iconSize: [41, 41],
                iconAnchor: [25, 25],
              })
              : " - ".split(" - ")[0] === marker.name
                ? new Icon({
                  iconUrl:
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Bluedot.svg/1024px-Bluedot.svg.png",
                  iconSize: [25, 25],
                  iconAnchor: [12, 12],
                })
                : new Icon({
                  iconUrl: markerIconPng,
                  iconSize: [25, 41],
                  iconAnchor: [12, 41],
                })
          }
        >
          <Popup>
            {marker?.name}. <br /> {marker?.desc}.
          </Popup>
        </Marker>
      ))}
      {polyline.map((polyline) => (
        <Polyline
          key={polyline.transport}
          pathOptions={{
            color:
              metroColors[polyline.transport] || "darkmagenta",
          }}
          positions={polyline.trips}
        />
      ))}
    </MapContainer>
  );
}